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

    author = relationship("User", foreign_keys=[author_id], overlaps="watchers,executors")
    responsible = relationship("User", foreign_keys=[responsible_id], overlaps="watchers,executors")

    watchers = relationship("User", secondary="task_watchers", lazy="selectin", overlaps="task_watchers,task_executors")
    executors = relationship("User", secondary="task_executors", lazy="selectin", overlaps="task_watchers,task_executors")


class TaskWatcher(BaseModel):
    __tablename__ = "task_watchers"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    task = relationship("Task", backref="task_watchers", overlaps="watchers,task_watchers")
    user = relationship("User", overlaps="watchers,task_watchers")


class TaskExecutor(BaseModel):
    __tablename__ = "task_executors"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    task = relationship("Task", backref="task_executors", overlaps="executors,task_executors")
    user = relationship("User", overlaps="executors,task_executors")