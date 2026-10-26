"""create users table

Revision ID: 0001_create_users
Revises:
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_users"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", sa.Enum("ZAKAZCHIK", "PEREVOZCHIK", name="userrole"), nullable=False),
        sa.Column("inn", sa.String(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("company_name", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("contact_person", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone"),
        sa.UniqueConstraint("inn"),
    )
    for column in ("id", "email", "phone", "inn"):
        op.create_index(op.f(f"ix_users_{column}"), "users", [column], unique=False)


def downgrade() -> None:
    op.drop_table("users")
