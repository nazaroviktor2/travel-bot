from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateItemRequest(BaseModel):
    name: str
    days_needed: int
    note: str | None


class ItemDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    note: str | None
    days_needed: int

    created_at: datetime
