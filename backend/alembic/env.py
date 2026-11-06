from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic import context

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.config.settings import settings  # noqa: E402
from src.app.db.base import Base  # noqa: E402
from src.modules.auth import models as auth_models  # noqa: E402,F401
from src.modules.bids import models as bid_models  # noqa: E402,F401
from src.modules.dictionaries import models as dictionary_models  # noqa: E402,F401
from src.modules.tenders import models as tender_models  # noqa: E402,F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    return settings.database_url


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=False,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(get_url(), poolclass=None)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
