"""create_comp_pos_tables

Revision ID: 7e2ee1e79cdc
Revises: 1b87872949d9
Create Date: 2024-07-25 10:45:44.649226

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7e2ee1e79cdc"
down_revision: Union[str, None] = "1b87872949d9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, nullable=False, unique=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("first_name", sa.String, nullable=True),
        sa.Column("last_name", sa.String, nullable=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("company_id", sa.Integer, sa.ForeignKey("companies.id")),
        sa.Column("department_id", sa.Integer, nullable=True),
        sa.Column("position_id", sa.Integer, sa.ForeignKey("positions.id")),
    )


def downgrade():
    op.drop_table("users")
