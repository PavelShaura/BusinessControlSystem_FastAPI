from fastapi import HTTPException

from src.api.v1.auth.utils.password_utils import hash_password
from src.schemas.company_schemas import CompleteSignUpResponse
from src.utils.logging_logic import logger


class CompleteSignUpService:
    @staticmethod
    async def complete_sign_up(uow, user_data):
        try:
            async with uow:
                existing_user = await uow.user_repository.get_by_email(user_data.account)
                if existing_user:
                    logger.info(f"User {existing_user} already exists")
                    raise ValueError("User already exists")

                company = await uow.company_repository.get_by_name(user_data.company_name)
                if not company:
                    company = await uow.company_repository.create(
                        name=user_data.company_name
                    )

                hashed_password = hash_password(user_data.password)
                new_user = await uow.user_repository.create(
                    email=user_data.account,
                    hashed_password=hashed_password,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    is_admin=True,
                    company_id=company.id,
                )

                await uow.commit()

                return CompleteSignUpResponse(
                    email=new_user.email,
                    password=hashed_password,
                    first_name=new_user.first_name,
                    last_name=new_user.last_name,
                    company_name=company.name,
                ).model_dump()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
