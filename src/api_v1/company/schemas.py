from pydantic import BaseModel, EmailStr


class CompanyCreate(BaseModel):
    name: str


class EmployeeCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str


class InviteResponse(BaseModel):
    message: str


class SignUpComplete(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str
