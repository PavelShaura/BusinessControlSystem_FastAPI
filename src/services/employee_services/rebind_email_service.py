import jwt

from fastapi import HTTPException, Depends

from src.api.v1.auth.utils.password_utils import validate_password
from src.utils.mail_utils.send_email_service import EmailService
from src.core.config import settings
from src.schemas.employee_schemas import RebindEmailResponse


class RebindEmailService:
    @staticmethod
    async def rebind_email(
        uow,
        new_email,
        current_password,
        request
    ):
        try:
            user_id = request.state.user.id

            async with uow:
                employee = await uow.user_repository.get_by_id(user_id)
                if not employee:
                    raise HTTPException(status_code=404, detail="Employee not found")

                if not validate_password(current_password, employee.hashed_password):
                    raise HTTPException(status_code=400, detail="Invalid password")

                existing_employee = await uow.user_repository.get_by_email(new_email)
                if existing_employee:
                    raise HTTPException(status_code=400, detail="Email already in use")

                rebind_token = jwt.encode(
                    {
                        "employee_id": employee.id,
                        "new_email": new_email,
                        "company_id": employee.company_id,
                    },
                    settings.auth_jwt.private_key_path.read_text(),
                    algorithm=settings.auth_jwt.algorithm,
                )

                rebind_url = f"{request.base_url}api/v1/employees/confirm-rebind-email?token={rebind_token}"
                email_service = EmailService()
                await email_service.send_rebind_email(new_email, rebind_url)

                return RebindEmailResponse(
                    message="Rebind email sent successfully", rebind_url=rebind_url
                ).model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
