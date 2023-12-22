#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Redis connection
"""

from redis import asyncio as aioredis
from redis.asyncio.client import Redis

from simpleo.core.config import settings

redis: Redis = aioredis.from_url(settings.REDIS_HTTP_URI)

