#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
News module endpoints
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from simpleo.auth.dependencies import AccessControl
from simpleo.auth.schemas import User

from simpleo.news.table_data_gateways.news import NewsTDG
from simpleo.news.schemas import (
    News,
    CreateNewsRequestSchema,
    CreateUpdateNewsResponseSchema,
    UpdateNewsRequestSchema,
    DeleteNewsResponseSchema
)

router = APIRouter()


@router.get("/", response_model=list[News])
async def get_news_filter(
        user_id: UUID | None = None,
        title: str | None = None,
):
    """
    Get news with filtering
    """
    if news := await NewsTDG().get(
        user_id=user_id,
        title=title
    ):
        return news
    raise HTTPException(
        status_code=500,
        detail="Internal server error."
    )


@router.get("/{news_uuid}", response_model=News)
async def get_news_by_uuid(
        news_uuid: UUID,
        user: User = Depends(AccessControl())
):
    """
    Get news by uuid
    """
    if news := await NewsTDG(user.id).get_by_uuid(news_uuid):
        return news
    return HTTPException(
        status_code=404,
        detail="News with entered uuid not found."
    )


@router.post("/", response_model=CreateUpdateNewsResponseSchema)
async def create_news(
        news_data: CreateNewsRequestSchema,
        user: User = Depends(AccessControl())
):
    """
    Create news
    """
    if news := await NewsTDG(user.id).create(user_id=user.id, **news_data.model_dump()):
        return news
    raise HTTPException(
        status_code=500,
        detail="Internal server error."
    )


@router.patch("/{news_uuid}", response_model=CreateUpdateNewsResponseSchema)
async def update_news(
        news_uuid: UUID,
        news_data: UpdateNewsRequestSchema,
        user: User = Depends(AccessControl())
):
    """
    Update news
    """
    if news := await NewsTDG(user.id).update(news_id=news_uuid, **news_data.model_dump()):
        return news
    raise HTTPException(
        status_code=500,
        detail="Internal server error."
    )


@router.delete("/{news_uuid}", response_model=DeleteNewsResponseSchema)
async def delete_news(
        news_uuid: UUID,
        user: User = Depends(AccessControl())
):
    """
    Delete news
    """
    if news_uuid := await NewsTDG(user.id).delete(news_id=news_uuid):
        return DeleteNewsResponseSchema(id=news_uuid)
    raise HTTPException(
        status_code=500,
        detail="Internal server error."
    )