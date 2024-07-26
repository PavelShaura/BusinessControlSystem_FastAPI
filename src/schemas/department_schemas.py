from typing import Optional, List

from pydantic import BaseModel

from src.schemas.base_schemas import MessageResponse


class ManagerInfo(BaseModel):
    manager_id: int
    manager_name: str


class AssignManager(BaseModel):
    manager_id: int

    class Config:
        from_attributes = True


class DepartmentMessageResponse(MessageResponse):
    pass


class DepartmentBase(BaseModel):
    name: str
    company_id: int
    parent: Optional[int] = None


class DepartmentCreate(BaseModel):
    name: str
    company_id: int
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class DepartmentUpdate(DepartmentBase):
    pass


class DepartmentResponse(BaseModel):
    id: int
    name: str
    company_id: int
    manager_info: Optional[ManagerInfo] = None

    class Config:
        from_attributes = True
