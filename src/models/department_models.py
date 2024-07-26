from sqlalchemy import (
    Column,
    Integer,
    String,
    Index,
    func,
    Sequence,
    ForeignKey,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

from src.core.database import engine
from src.models.base_model import BaseModel

id_seq = Sequence("departments_id_seq")


class Department(BaseModel):
    __tablename__ = "departments"

    id = Column(Integer, id_seq, primary_key=True, server_default=id_seq.next_value())
    name = Column(String, nullable=False)
    path = Column(LtreeType, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    company = relationship("Company", back_populates="departments")
    manager = relationship("User", foreign_keys=[manager_id])
    employees = relationship(
        "User", back_populates="department", foreign_keys="User.department_id"
    )

    parent = relationship(
        "Department",
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref="children",
        viewonly=True,
    )

    @classmethod
    async def create(cls, name, company_id, parent=None):
        async with AsyncSession(engine) as session:
            result = await session.execute(select(id_seq))
            _id = result.scalar_one()
            ltree_id = Ltree(str(_id))
            path = ltree_id if parent is None else parent.path + ltree_id
            new_department = cls(id=_id, name=name, company_id=company_id, path=path)
            session.add(new_department)
            await session.commit()
            return new_department

    __table_args__ = (Index("ix_departments_path", path, postgresql_using="gist"),)
