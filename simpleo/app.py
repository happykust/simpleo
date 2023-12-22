#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Project entrypoint
"""

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from simpleo.core.config import settings
from simpleo.core.router import router

from simpleo.core.connections.edgedb import client as database_client

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router)


@app.on_event("shutdown")
async def shutdown() -> None:
    """
    Shutdown function:
        Close all connections.
    :return:
    """
    await database_client.aclose()
