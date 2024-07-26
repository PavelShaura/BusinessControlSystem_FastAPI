import jwt

from fastapi import HTTPException

from src.api.v1.auth.utils.password_utils import validate_password
from src.api.v1.company.utils.email_utils import send_rebind_email
from src.core.config import settings
from src.services.base_service import BaseService
from src.schemas.employee_schemas import RebindEmailRequest, RebindEmailResponse


class RebindEmailService(BaseService):
    try:

        async def execute(self, uow, **kwargs):
            request_data = RebindEmailRequest(**kwargs)
            new_email = request_data.new_email
            current_password = request_data.current_password
            request = request_data.request

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

                await send_rebind_email(new_email, rebind_url)

                return RebindEmailResponse(
                    message="Rebind email sent successfully", rebind_url=rebind_url
                ).model_dump()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
