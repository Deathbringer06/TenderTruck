"""Stage 2: auto_bids

Revision ID: 003_stage2
Revises: 002_companies
"""
import sqlalchemy as sa
from alembic import op

revision = "003_stage2"
down_revision = "002_companies"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "auto_bids",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("tender_id", sa.Uuid(), sa.ForeignKey("tenders.id"), nullable=False),
        sa.Column("carrier_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("min_price", sa.Integer(), nullable=False),
        sa.Column("step", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_auto_bids_tender_id", "auto_bids", ["tender_id"])
    op.create_index("ix_auto_bids_carrier_id", "auto_bids", ["carrier_id"])

def downgrade() -> None:
    op.drop_table("auto_bids")