#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Auth module endpoints
"""

import datetime

from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRouter

from simpleo.auth import schemas, security
from simpleo.auth.dependencies import AccessControl
from simpleo.auth.schemas import RefreshTokenSchema
from simpleo.auth.security import decode_token, check_and_revoke_refresh_token, TokenTypeEnum, get_password_hash
from simpleo.auth.table_data_gateways.user import UserTDG

router = APIRouter()


@router.post('/login', response_model=schemas.AuthTokens)
async def login(
        login_data: schemas.UserLoginRequestSchema,
) -> schemas.AuthTokens:
    """
    Login user and return access and refresh tokens
    """
    user = await UserTDG().get_by_username(login_data.username)
    if not user or not await security.verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    return await security.generate_auth_tokens(user.id)


@router.post('/register', response_model=schemas.AuthTokens)
async def register(
        register_data: schemas.UserCreateRequestSchema,
) -> schemas.AuthTokens:
    """
    Register user and return access and refresh tokens
    """
    if await UserTDG().get_by_username(register_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with entered username exists in database"
        )

    register_data.password = await get_password_hash(register_data.password)

    if not (user := await UserTDG().create(user=register_data)):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal server error")
    return await security.generate_auth_tokens(user.id)


@router.post("/logout", response_model=dict)
async def logout(*, form_data: RefreshTokenSchema) -> dict:
    success, token_data = await decode_token(TokenTypeEnum.REFRESH, form_data.refresh_token)
    if success and token_data.exp > datetime.datetime.now().timestamp():
        await check_and_revoke_refresh_token(form_data.refresh_token)
    return {"detail": "Logged out."}


@router.get('/me', response_model=schemas.User)
def get_me(
        user: schemas.User = Depends(AccessControl())
) -> schemas.User:
    """
    Return current user
    """
    return user
