from typing import Optional, List

from pydantic import BaseModel

from src.schemas.base_schemas import MessageResponse


class AssignManager(BaseModel):
    manager_id: int

    class Config:
        orm_mode = True


class DepartmentMessageResponse(MessageResponse):
    pass


class DepartmentBase(BaseModel):
    name: str
    company_id: int
    parent_id: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    path: str
    manager_id: Optional[int] = None
    children: Optional[List["DepartmentResponse"]] = []

    class Config:
        orm_mode = True
