#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Base for Table Data Gateways
"""

import uuid

from edgedb import AsyncIOClient

from simpleo.core.connections.edgedb import client as database_client


class BaseTableDataGateway:
    """
    Base class for table data gateways.
    """

    __slots__ = "database"

    def __init__(self, user_id: uuid.UUID | None = None) -> None:
        """
        Set-up globals if it provided
        :param user_id:
        """
        if user_id:
            self.database: AsyncIOClient = database_client.with_globals({
                "auth::current_user_id": user_id
            })
        else:
            self.database: AsyncIOClient = database_client
