from src.api.v1.auth.utils.password_utils import hash_password
from src.services.base_service import BaseService


class CompleteSignUpService(BaseService):
    async def execute(self, uow, **kwargs):
        user_data = kwargs.get("user_data")
        async with uow:
            existing_user = await uow.user_repository.get_by_email(user_data.account)
            if existing_user:
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

            return {
                "email": new_user.email,
                "password": hashed_password,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "company_name": company.name,
            }
