from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class UserInfo(BaseModel):
    id: int
    email: str


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    watchers: List[int] = Field(default_factory=list)
    executors: List[int] = Field(default_factory=list)
    deadline: Optional[datetime] = None
    estimated_time: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    responsible_id: Optional[int] = None
    watchers: Optional[List[int]] = None
    executors: Optional[List[int]] = None
    deadline: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    estimated_time: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author: UserInfo
    responsible: Optional[UserInfo]
    watchers: List[UserInfo]
    executors: List[UserInfo]
    deadline: Optional[datetime]
    status: TaskStatus
    estimated_time: Optional[int]

    class Config:
        from_attributes = True
