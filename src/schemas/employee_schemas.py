from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from fastapi import Request


class CreateEmployeeRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


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


class EmployeeMessageResponse(BaseModel):
    message: str


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
    request: Request

    class Config:
        arbitrary_types_allowed = True


class RebindEmailResponse(BaseModel):
    message: str
    rebind_url: str


class UpdateEmployeeDataRequest(BaseModel):
    first_name: Optional[str] = Field(
        None, description="New first name of the employee"
    )
    last_name: Optional[str] = Field(None, description="New last name of the employee")
    current_password: str = Field(..., description="Current password of the employee")
    request: Request

    class Config:
        arbitrary_types_allowed = True
