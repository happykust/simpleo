#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
EdgeDB connection
"""

from edgedb import create_async_client, AsyncIOClient

from simpleo.core.config import settings

client: AsyncIOClient = create_async_client(settings.DB_HTTP_URI, tls_ca_file=settings.DB_TLS_FILE_PATH)
