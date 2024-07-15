from datetime import datetime
from typing import Annotated
from annotated_types import MinLen, MaxLen

from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True


class UserInfo(BaseModel):
    username: str
    email: EmailStr
    logged_in_at: datetime

    class Config:
        from_attributes = True