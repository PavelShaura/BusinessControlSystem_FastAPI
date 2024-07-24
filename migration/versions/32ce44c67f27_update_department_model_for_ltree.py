"""update department model for ltree

Revision ID: 32ce44c67f27
Revises: b41b2cc45284
Create Date: 2024-07-24 12:23:13.670495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32ce44c67f27'
down_revision: Union[str, None] = 'b41b2cc45284'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('departments_company_id_fkey', 'departments', type_='foreignkey')
    op.drop_constraint('departments_manager_id_fkey', 'departments', type_='foreignkey')
    op.create_foreign_key(None, 'departments', 'users', ['manager_id'], ['id'])
    op.create_foreign_key(None, 'departments', 'companies', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'departments', type_='foreignkey')
    op.drop_constraint(None, 'departments', type_='foreignkey')
    op.create_foreign_key('departments_manager_id_fkey', 'departments', 'users', ['manager_id'], ['id'], deferrable=True)
    op.create_foreign_key('departments_company_id_fkey', 'departments', 'companies', ['company_id'], ['id'], deferrable=True)
    # ### end Alembic commands ###