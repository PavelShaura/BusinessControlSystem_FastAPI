from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models.base_model import BaseModel


class Company(BaseModel):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    employees = relationship("User", back_populates="company")
    departments = relationship("Department", back_populates="company")
    positions = relationship("Position", back_populates="company")
