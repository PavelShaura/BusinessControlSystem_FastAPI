"""create users table

Revision ID: d2920957faad
Revises: 655060673ff7
Create Date: 2024-07-24 12:12:23.649911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2920957faad'
down_revision: Union[str, None] = '655060673ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('first_name', sa.String, nullable=True),
        sa.Column('last_name', sa.String, nullable=True),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_admin', sa.Boolean, default=False),
        sa.Column('company_id', sa.Integer, sa.ForeignKey('companies.id')),
        sa.Column('department_id', sa.Integer, nullable=True),
        sa.Column('position_id', sa.Integer, sa.ForeignKey('positions.id')),
    )


def downgrade():
    op.drop_table('users')