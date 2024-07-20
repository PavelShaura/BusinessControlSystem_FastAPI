from pydantic import BaseModel, EmailStr


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
