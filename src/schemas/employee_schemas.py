from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from fastapi import Request

from src.schemas.base_schemas import MessageResponse


class CreateEmployeeRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    position_id: Optional[int]


class EmployeeResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    company_id: int
    is_active: bool


class EmployeeRegistrationCompleteSchema(BaseModel):
    employee_id: int
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    token: str


class EmployeeMessageResponse(MessageResponse):
    pass


class EmployeeRegistrationCompleteRequest(BaseModel):
    password: str
    password_confirm: str
    token: str


class EmployeeDataResponse(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool
    is_active: bool
    company_id: int


class EmployeeRegistrationCompleteResponse(BaseModel):
    message: str
    data: EmployeeDataResponse


class GenerateURLEmployeeInviteResponse(BaseModel):
    message: str
    invite_url: str


class RebindEmailRequest(BaseModel):
    new_email: EmailStr
    current_password: str


class RebindEmailResponse(BaseModel):
    message: str
    rebind_url: str


class UpdateEmployeeDataRequest(BaseModel):
    first_name: Optional[str] = Field(
        None, description="New first name of the employee"
    )
    last_name: Optional[str] = Field(None, description="New last name of the employee")
    position_id: Optional[int] = Field(
        None, description="New position ID of the employee"
    )
    current_password: str = Field(..., description="Current password of the employee")
