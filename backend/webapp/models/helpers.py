from typing import Annotated

from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column

created_at = Annotated[DateTime, mapped_column(DateTime(timezone=True), default=func.now())]
deleted_at = Annotated[DateTime, mapped_column(DateTime(timezone=True), nullable=True)]
is_deleted = Annotated[bool, mapped_column(nullable=False, default=False)]
