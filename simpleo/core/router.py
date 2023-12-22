#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
General project routing
"""

from fastapi.routing import APIRouter

from simpleo.auth.endpoints import router as auth_router
from simpleo.news.endpoints import router as news_router
from simpleo.core.config import settings

router = APIRouter(prefix=settings.API_V1_STR)
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(news_router, prefix="/news", tags=["News"])


