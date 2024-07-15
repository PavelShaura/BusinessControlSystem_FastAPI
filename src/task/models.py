from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.utils.base_model import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    responsible_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(DateTime)
    status = Column(String)
    estimated_time = Column(Integer)  # в минутах

    author = relationship("User", foreign_keys=[author_id], back_populates="created_tasks")
    responsible = relationship("User", foreign_keys=[responsible_id], back_populates="assigned_tasks")
    observers = relationship("User", secondary="task_observers")
    executors = relationship("User", secondary="task_executors")


# Связующие таблицы для задач
task_observers = Table('task_observers', Base.metadata,
                       Column('task_id', Integer, ForeignKey('tasks.id')),
                       Column('user_id', Integer, ForeignKey('users.id'))
                       )

task_executors = Table('task_executors', Base.metadata,
                       Column('task_id', Integer, ForeignKey('tasks.id')),
                       Column('user_id', Integer, ForeignKey('users.id'))
                       )