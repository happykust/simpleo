#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

from uuid import UUID

import edgedb.errors

from simpleo.core.connections.table_data_gateways import BaseTableDataGateway
from simpleo.news.schemas import News


class NewsTDG(BaseTableDataGateway):
    """
    News TDG
    """

    async def get(self,
                  user_id: UUID | None = None,
                  title: str | None = None) -> list[News] | None:
        """
        Get news by filtering
        """
        query = """
        with
            user_id := <optional uuid>$user_id,
            title := <optional str>$title
        select news::News {*, user: {*}}
            filter
                (.title ?= title or title ?= <optional str>{})
                and
                (.user ?= (select detached auth::User filter .id = user_id) or user_id ?= <optional uuid>{})
        """

        try:
            return await self.database.query(query, user_id=user_id, title=title)
        except edgedb.errors.EdgeDBError as e:
            return None

    async def get_by_uuid(self, news_id: UUID) -> News | None:
        """
        Get news by uuid
        """
        query = """
        select news::News {*, user: {*}} filter .id = <uuid>$news_id
        """

        try:
            if news := await self.database.query(query, news_id=news_id):
                return news[0]
            return None
        except edgedb.errors.EdgeDBError:
            return None

    async def create(self,
                     user_id: UUID,
                     title: str,
                     content: str) -> News | None:
        """
        Create news
        """
        query = """
        with
            user_id := <uuid>$user_id,
            title := <str>$title,
            content := <str>$content
        select (insert news::News {
            user := (select detached auth::User filter .id = user_id),
            title := title,
            content := content
        }) {*}
        """

        try:
            return (await self.database.query(query, user_id=user_id, title=title, content=content))[0]
        except edgedb.errors.EdgeDBError:
            return None

    async def update(self,
                     news_id: UUID,
                     title: str | None = None,
                     content: str | None = None) -> News | None:
        """
        Update news
        """
        query = """
        with
            news_id := <uuid>$news_id,
            title := <optional str>$title,
            content := <optional str>$content
        select (update news::News filter .id = news_id set {
            title := title ?? .title,
            content := content ?? .content
        }) {*}
        """

        try:
            return (await self.database.query(query, news_id=news_id, title=title, content=content))[0]
        except edgedb.errors.EdgeDBError:
            return None

    async def delete(self, news_id: UUID) -> UUID | None:
        """
        Delete news
        """
        query = """
        delete news::News filter .id = <uuid>$news_id
        """

        try:
            await self.database.query(query, news_id=news_id)
            return news_id
        except edgedb.errors.EdgeDBError:
            return None
