"""create companies and positions tables

Revision ID: 655060673ff7
Revises: 
Create Date: 2024-07-24 12:11:23.381170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '655060673ff7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
    )

    op.create_table(
        'positions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('company_id', sa.Integer, sa.ForeignKey('companies.id')),
    )


def downgrade():
    op.drop_table('positions')
    op.drop_table('companies')
