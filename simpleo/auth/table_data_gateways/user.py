#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Implementation Table Data Gateway pattern for User essence
"""

import uuid

import edgedb.errors

from simpleo.auth.schemas import (
    User,
    UserCreateRequestSchema
)
from simpleo.core.connections.table_data_gateways import BaseTableDataGateway
from simpleo.core.utils import make_pydantic_model


class UserTDG(BaseTableDataGateway):
    """
    User TDG
    """

    async def get_all(self, limit: int = 20, offset: int = 0) -> list[User]:
        """
        Get all users from db
        :return:
        """
        query = """
        select auth::User { * } offset <int64>$offset limit <int64>$limit
        """
        return await self.database.query(query, limit=limit, offset=offset)

    async def get_by_username(self, username: str = "") -> User | None:
        """
        Get user by username if exist else None
        :param username:
        :return:
        """
        query = """
        select auth::User { * } filter .username ?= <str>$username
        """
        if result := await self.database.query(query, username=username):
            return result[0]
        return None

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """
        Get user by id
        :param user_id:
        :return:
        """
        query = """
        select auth::User { * } filter .id = <uuid>$user_id
        """
        if result := await self.database.query(query, user_id=user_id):
            return make_pydantic_model(User, result[0])
        return None

    async def get_current_user(self) -> User | None:
        """
        Get current user by global variable
        :return:
        """
        query = """
        select global auth::current_user {*};
        """
        if result := await self.database.query(query):
            return make_pydantic_model(User, result[0])
        return None

    async def create(self, user: UserCreateRequestSchema) -> User | None:
        """
        Create new user
        :param user:
        :return:
        """
        query = """
        with
            username := <str>$username,
            email := <str>$email,
            password := <str>$password
        select (insert auth::User {
            password := password,
            username := username,
            email := email
        }) {*}
        """

        try:
            created_user = (await self.database.query(query, **user.model_dump()))[0]
        except edgedb.errors.ConstraintViolationError:
            return None
        return created_user
