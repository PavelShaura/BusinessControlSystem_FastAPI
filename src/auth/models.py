from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.core.database import Base
from src.utils.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    companies = relationship("Company", secondary="members", back_populates="users")
    created_tasks = relationship("Task", back_populates="author", foreign_keys="Task.author_id")
    assigned_tasks = relationship("Task", back_populates="responsible", foreign_keys="Task.responsible_id")

# Связующая таблица для отношения многие-ко-многим между User и Company
members = Table('members', Base.metadata,
                Column('user_id', Integer, ForeignKey('users.id')),
                Column('company_id', Integer, ForeignKey('companies.id'))
                )