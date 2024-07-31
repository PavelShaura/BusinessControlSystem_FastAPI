import jwt

from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from src.core.config import settings


class ShowRegistrationFormService:
    @staticmethod
    async def show_form(uow, token) -> HTMLResponse:
        try:
            payload = jwt.decode(
                token,
                settings.auth_jwt.public_key_path.read_text(),
                algorithms=[settings.auth_jwt.algorithm],
            )
            email = payload["email"]
            async with uow:
                employee = await uow.user_repository.get_by_email(email)
                if not employee:
                    raise HTTPException(status_code=404, detail="Employee not found")
                if employee.is_active:
                    raise HTTPException(
                        status_code=400, detail="Employee already registered"
                    )
        except jwt.PyJWTError:
            raise HTTPException(status_code=400, detail="Invalid token")

        html_content = f"""
            <form method="post">
                <input type="hidden" name="token" value="{token}">
                <p>Email: {email}</p>
                <input type="password" name="password" placeholder="Password" required>
                <input type="password" name="password_confirm" placeholder="Confirm Password" required>
                <button type="submit">Complete Registration</button>
            </form>
            """
        return HTMLResponse(content=html_content)
