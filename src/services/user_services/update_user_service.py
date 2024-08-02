from fastapi import HTTPException

from src.models.department_models import Department
from src.models.position_models import Position
from src.schemas.user_schemas import UserUpdate, UserResponse


class UpdateUserService:
    @staticmethod
    async def update_user(uow, user_id: int, update_data: UserUpdate):
        try:
            async with uow:
                user = await uow.user_repository.get_by_id(user_id)
                if not user:
                    raise ValueError("User not found")

                field_repo_map = {
                    "department_id": (uow.department_repository, Department),
                    "position_id": (uow.position_repository, Position),
                }

                for field, (repo, model) in field_repo_map.items():
                    field_value = getattr(update_data, field)
                    if field_value:
                        entity = await repo.get_by_id(field_value)
                        if not entity:
                            raise ValueError(f"{model.__name__} not found")
                        setattr(user, field, field_value)

                await uow.user_repository.update(user)
                await uow.commit()

                return UserResponse.model_validate(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
