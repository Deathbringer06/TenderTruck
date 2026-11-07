import sqlalchemy as sa

from alembic import op

revision = "002_companies"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("owner_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("inn", sa.String(length=12), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column(
            "verification_status",
            sa.Enum("PENDING", "VERIFIED", "REJECTED", name="verificationstatus"),
            server_default="PENDING",
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_companies_owner_id", "companies", ["owner_id"])


def downgrade() -> None:
    op.drop_index("ix_companies_owner_id", table_name="companies")
    op.drop_table("companies")
    sa.Enum(name="verificationstatus").drop(op.get_bind(), checkfirst=True)
