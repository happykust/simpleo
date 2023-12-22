#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023
from uuid import UUID

from pydantic import BaseModel

from simpleo.core.schemas import Auditable
from simpleo.auth.schemas import User


class News(Auditable):
    """
    News schema
    """
    user: User
    title: str
    content: str


class CreateNewsRequestSchema(BaseModel):
    """
    CreateNewsRequest schema
    """
    title: str
    content: str


class CreateUpdateNewsResponseSchema(Auditable):
    """
    CreateNewsResponse schema
    """
    title: str
    content: str


class UpdateNewsRequestSchema(BaseModel):
    """
    UpdateNewsRequest schema
    """
    title: str | None = None
    content: str | None = None


class DeleteNewsResponseSchema(BaseModel):
    """
    DeleteNewsResponse schema
    """
    id: UUID
