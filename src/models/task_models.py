from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from src.models.base_model import BaseModel

from enum import Enum


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(BaseModel):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    responsible_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(DateTime)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    estimated_time = Column(Integer)  # в минутах

    author = relationship("User", foreign_keys=[author_id])
    responsible = relationship("User", foreign_keys=[responsible_id])

    watchers = association_proxy("task_watchers", "user")
    executors = association_proxy("task_executors", "user")


class TaskWatcher(BaseModel):
    __tablename__ = "task_watchers"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    task = relationship("Task", backref="task_watchers")
    user = relationship("User")


class TaskExecutor(BaseModel):
    __tablename__ = "task_executors"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    task = relationship("Task", backref="task_executors")
    user = relationship("User")