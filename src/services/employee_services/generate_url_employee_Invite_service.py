import jwt

from fastapi import HTTPException, Depends

from src.utils.mail_utils.send_email_service import EmailService
from src.core.config import settings
from src.schemas.employee_schemas import GenerateURLEmployeeInviteResponse


class GenerateURLEmployeeInviteService:
    @staticmethod
    async def generate_url_employee_invite(
        uow, employee_id, request, email_service: EmailService = Depends(EmailService)
    ):
        try:
            async with uow:
                employee = await uow.user_repository.get_by_id(employee_id)
                if not employee:
                    raise HTTPException(status_code=404, detail="Employee not found")

                invite_token = jwt.encode(
                    {
                        "employee_id": employee.id,
                        "email": employee.email,
                        "company_id": employee.company_id,
                    },
                    settings.auth_jwt.private_key_path.read_text(),
                    algorithm=settings.auth_jwt.algorithm,
                )

                invite_url = f"{request.base_url}api/v1/employees/registration-complete?token={invite_token}"

                await email_service.send_initial_invite_email(
                    employee.email, invite_url
                )

                return GenerateURLEmployeeInviteResponse(
                    message="Invite sent successfully", invite_url=invite_url
                ).model_dump()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
