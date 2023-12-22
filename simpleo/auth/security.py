#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023
#
#

"""
Security functions
"""

import binascii
import enum
import json
from datetime import datetime, timedelta
from typing import Any

import pyseto
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import ValidationError

from simpleo.auth import schemas
from simpleo.auth.schemas import TokenPayloadSchema
from simpleo.core.config import settings
from simpleo.core.connections.redis import redis

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


class TokenTypeEnum(enum.Enum):
    """
    Types of auth tokens
    """
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


async def check_and_revoke_refresh_token(token: str) -> bool:
    """
    Check if refresh token in blacklist.
    If refresh token not in blacklist it will put token to blacklist.
    :param token:
    :return:
    """
    is_token_in_blacklist = await redis.sismember("refresh-token-blacklist", token)
    if is_token_in_blacklist:
        return True
    adding_status = await redis.sadd("refresh-token-blacklist", token)
    if adding_status == 0:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Something went wrong. Try again later.",
        )
    return False


async def decode_token(token_type: TokenTypeEnum, token: str) -> tuple[bool, None | TokenPayloadSchema]:
    """
    Decode access/refresh token and return token payload
    :param token_type:
    :param token:
    :return:
    """
    private_key = settings.__dict__[f"PRIVATE_PUBLIC_{token_type.value}_KEY"]
    try:
        payload = json.loads(pyseto.decode(private_key, token).payload.decode("utf-8"))
        token_data = schemas.TokenPayloadSchema(**payload)
    except (pyseto.DecryptError,
            pyseto.VerifyError,
            ValidationError,
            binascii.Error,
            ValueError):
        return False, None
    return True, token_data


async def create_token(token_type: TokenTypeEnum,
                       subject: Any,
                       expires_delta: timedelta | None = None) -> str:
    """
    Create and return access/refresh paseto token.
    :param token_type:
    :param subject:
    :param expires_delta:
    :return:
    """
    private_key = settings.__dict__[f"PRIVATE_SECRET_{token_type.value}_KEY"]
    expire_key_minutes = settings.__dict__.get(f"{token_type.value}_TOKEN_EXPIRE_MINUTES", None)

    expire = None
    if expires_delta:
        expire = datetime.now() + expires_delta
    elif expire_key_minutes:
        expire = datetime.now() + timedelta(
            minutes=expire_key_minutes
        )

    to_encode = {
        "exp": expire.timestamp() if expire else None,
        "sub": str(subject)
    }
    return pyseto.encode(private_key, json.dumps(to_encode)).decode("utf-8")


async def generate_auth_tokens(subject: Any) -> schemas.AuthTokens:
    """
    Generate a pair of tokens and return it
    :param subject:
    :return:
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return schemas.AuthTokens(
        access_token=await create_token(TokenTypeEnum.ACCESS, subject, expires_delta=access_token_expires),
        refresh_token=await create_token(TokenTypeEnum.REFRESH, subject, expires_delta=refresh_token_expires),
        token_type="bearer"
    )


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifying plain password with hashed password.
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """
    Hash incoming password.
    :param password:
    :return:
    """
    return pwd_context.hash(password)
