from pydantic import BaseModel, EmailStr


class MessageResponse(BaseModel):
    message: str


class SignUpRequest(BaseModel):
    email: EmailStr

class SignUpResponse(BaseModel):
    message: str
    email: EmailStr

class CompleteSignUpRequest(BaseModel):
    account: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str


class CompleteSignUpResponse(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str

class VerifySignUpRequest(BaseModel):
    email: EmailStr
    invite_token: str
