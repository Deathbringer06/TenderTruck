from __future__ import annotations

import uuid
from datetime import UTC, datetime

import sqlalchemy as sa

from alembic import op

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("customer", "carrier", "admin", name="userrole"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "tenders",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("start_price", sa.Integer(), nullable=False),
        sa.Column("current_price", sa.Integer(), nullable=False),
        sa.Column("step", sa.Integer(), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "status",
            sa.Enum("DRAFT", "ACTIVE", "CLOSED", name="tenderstatus"),
            nullable=False,
        ),
        sa.Column("extension_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("max_extensions", sa.Integer(), server_default="10", nullable=False),
        sa.Column("created_by", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "bids",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("tender_id", sa.Uuid(), sa.ForeignKey("tenders.id"), nullable=False),
        sa.Column("carrier_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("is_winner", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("tender_id", "idempotency_key", name="uq_bid_idempotency"),
    )
    op.create_index("ix_bids_tender_id", "bids", ["tender_id"])
    op.create_index("ix_bids_carrier_id", "bids", ["carrier_id"])

    op.create_table(
        "dictionaries",
        sa.Column("id", sa.Uuid(), primary_key=True, nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("category", "code", name="uq_dictionary_category_code"),
    )
    op.create_index("ix_dictionaries_category", "dictionaries", ["category"])

    now = datetime.now(UTC)
    op.bulk_insert(
        sa.table(
            "dictionaries",
            sa.column("id", sa.Uuid()),
            sa.column("category", sa.String()),
            sa.column("code", sa.String()),
            sa.column("name", sa.String()),
            sa.column("is_active", sa.Boolean()),
            sa.column("created_at", sa.DateTime(timezone=True)),
            sa.column("updated_at", sa.DateTime(timezone=True)),
        ),
        [
            {
                "id": uuid.uuid4(),
                "category": category,
                "code": code,
                "name": name,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            }
            for category, values in {
                "body_types": {
                    "tent": "Tent",
                    "refrigerator": "Refrigerator",
                },
                "currencies": {
                    "KGS": "Kyrgyz som",
                    "USD": "US dollar",
                },
            }.items()
            for code, name in values.items()
        ],
    )


def downgrade() -> None:
    op.drop_table("dictionaries")
    op.drop_table("bids")
    op.drop_table("tenders")
    op.drop_table("users")
    sa.Enum(name="tenderstatus").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="userrole").drop(op.get_bind(), checkfirst=True)
