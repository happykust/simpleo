#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Decorators depends on auth processes for usage anywhere.
"""

import uuid
import datetime

from fastapi import HTTPException, status, Depends

from simpleo.auth import security, schemas
from simpleo.auth.table_data_gateways.user import UserTDG


class AccessControl:
    """
    Helps ensure that request sent from authenticated user.
    Use this with Depends() and make sure that you call this!

    Default usage:
        @app.post('/some-url')
        async def some_func(user: User = Depends(AccessControl())):
            return f"Hello, world! I'm user - {user.username}"

    """

    async def process(self, token: str) -> schemas.User:
        """
        Check user
        :return:
        """
        success, token_data = await security.decode_token(security.TokenTypeEnum.ACCESS, token)
        if not success or token_data.exp < datetime.datetime.now().timestamp():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not (user := await UserTDG(user_id=token_data.sub).get_current_user()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        return user

    async def __call__(self, token: str = Depends(security.reusable_oauth2)) -> schemas.User:
        """
        Call main process function
        :param token:
        :return:
        """
        return await self.process(token)
