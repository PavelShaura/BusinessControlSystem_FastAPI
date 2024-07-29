from fastapi import HTTPException

from src.services.base_service import BaseService
from src.schemas.task_schemas import TaskUpdate, TaskResponse


class UpdateTaskService(BaseService):
    try:
        # TODO
        pass
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
