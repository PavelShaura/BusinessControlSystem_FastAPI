from typing import Optional

from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class EmployeeRegistrationCompleteSchema(BaseModel):
    employee_id: int
    email: EmailStr
    password: str


class EmployeeUpdate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    current_password: str
