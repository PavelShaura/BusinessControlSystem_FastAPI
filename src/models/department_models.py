from sqlalchemy import Column, Integer, String, ForeignKey, Index, func
from sqlalchemy.orm import relationship, foreign, remote
from sqlalchemy.sql.expression import cast
from sqlalchemy_utils import LtreeType

from src.models.base_model import BaseModel


class Department(BaseModel):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(LtreeType, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    company = relationship("Company", back_populates="departments")
    manager = relationship("User", foreign_keys=[manager_id])
    employees = relationship("User", back_populates="department", foreign_keys="User.department_id")

    parent = relationship(
        'Department',
        primaryjoin=cast(func.subpath(foreign(path), 0, -1), LtreeType) == cast(remote(path), LtreeType),
        remote_side=[path],
        backref='children',
        viewonly=True,
    )

    __table_args__ = (
        Index('ix_departments_path', path, postgresql_using="gist"),
    )

    def __init__(self, name, company_id, parent=None):
        self.name = name
        self.company_id = company_id
        if parent:
            self.path = parent.path + '.' + str(self.id)
        else:
            self.path = str(self.id)
