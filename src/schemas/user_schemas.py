from pydantic import BaseModel
from typing import Optional


class UserUpdate(BaseModel):
    department_id: Optional[int]
    position_id: Optional[int]

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_admin: bool
    company_id: Optional[int]
    department_id: Optional[int]
    position_id: Optional[int]

    class Config:
        from_attributes = True
