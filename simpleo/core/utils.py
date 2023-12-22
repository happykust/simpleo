#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Shared utils
"""

import uuid
from typing import TypeVar, Type, Annotated

import edgedb
from fastapi import HTTPException, status, UploadFile

PD_MODEL_TYPE = TypeVar("PD_MODEL_TYPE")


def make_pydantic_model(model: Type[PD_MODEL_TYPE], obj: edgedb.Object) -> PD_MODEL_TYPE:
    """
    Make pydantic model from EdgeDB Object
    :param model:
    :param obj:
    :return:
    """
    return model.model_validate({arg: obj.__getattribute__(arg) for arg in obj.__dir__()})
