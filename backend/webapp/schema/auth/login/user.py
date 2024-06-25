from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserLogin(BaseModel):
    id: int


class UserLoginResponse(BaseModel):
    access_token: str


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
