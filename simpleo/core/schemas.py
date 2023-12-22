#  Copyright (C) Simpleo - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by happykust - Kirill Nikolaevskiy <happykust@list.ru>, 2023

"""
Shared schemas
"""

import datetime
import uuid

from pydantic import BaseModel


class Auditable(BaseModel):
    """
    Auditable share schema
    """
    id: uuid.UUID
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
