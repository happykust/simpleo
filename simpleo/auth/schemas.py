#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Auth module schemas
"""

import uuid

from pydantic import (
    Field,
    BaseModel,
)

from simpleo.core.schemas import Auditable


class User(Auditable):
    """
    User schema
    """
    id: uuid.UUID
    username: str | None = Field(None)
    email: str | None = Field(None)
    password: str = Field(exclude=True)


class UserCreateRequestSchema(BaseModel):
    """
    User create request schema
        login: can be email or telephone
    """
    username: str = Field(min_length=3, max_length=30)
    email: str = Field(min_length=4)
    password: str = Field(min_length=8)


class AuthTokens(BaseModel):
    """
    Pair of auth tokens schema
    """
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenSchema(BaseModel):
    """
    Refresh token schema
    """
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    """
    Token payload schema
    """
    exp: float
    sub: uuid.UUID


class UserLoginRequestSchema(BaseModel):
    """
    User login request schema
    """
    username: str
    password: str
