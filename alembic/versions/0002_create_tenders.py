"""add tenders table

Revision ID: 0002_create_tenders
Revises: 0001_create_users
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_create_tenders"
down_revision: Union[str, None] = "0001_create_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tenders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("point_a", sa.String(length=255), nullable=False),
        sa.Column("point_b", sa.String(length=255), nullable=False),
        sa.Column("cargo_weight", sa.Float(), nullable=True),
        sa.Column("cargo_volume", sa.Float(), nullable=True),
        sa.Column("body_type", sa.String(length=100), nullable=True),
        sa.Column("loading_date", sa.DateTime(), nullable=False),
        sa.Column("unloading_date", sa.DateTime(), nullable=True),
        sa.Column("start_price", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tenders_id"), "tenders", ["id"], unique=False)
    op.create_index(op.f("ix_tenders_customer_id"), "tenders", ["customer_id"], unique=False)
    op.create_index(op.f("ix_tenders_status"), "tenders", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tenders_status"), table_name="tenders")
    op.drop_index(op.f("ix_tenders_customer_id"), table_name="tenders")
    op.drop_index(op.f("ix_tenders_id"), table_name="tenders")
    op.drop_table("tenders")
