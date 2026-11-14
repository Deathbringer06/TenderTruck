"""Add company INN scoring history."""

import sqlalchemy as sa

from alembic import op

revision = "004_stage2_rest"
down_revision = "003_stage2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "company_scores",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("company_id", sa.Uuid(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column(
            "risk_level",
            sa.Enum("LOW", "MEDIUM", "HIGH", name="risklevel"),
            nullable=False,
        ),
        sa.Column(
            "checked_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_company_scores_company_id", "company_scores", ["company_id"])


def downgrade() -> None:
    op.drop_index("ix_company_scores_company_id", table_name="company_scores")
    op.drop_table("company_scores")
    sa.Enum(name="risklevel").drop(op.get_bind(), checkfirst=True)
