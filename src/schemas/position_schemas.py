from pydantic import BaseModel

from src.schemas.base_schemas import MessageResponse


class PositionMessageResponse(MessageResponse):
    pass


class PositionBase(BaseModel):
    name: str
    company_id: int


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionResponse(PositionBase):
    id: int

    class Config:
        from_attributes = True
