from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: str
    password: bytes
    is_admin: bool
    company_id: int
    email: EmailStr | None = None
    is_active: bool = True
