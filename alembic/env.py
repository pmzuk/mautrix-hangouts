from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

import sys
from os.path import abspath, dirname

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from mautrix.util.db import Base
from mautrix_hangouts.config import Config
import mautrix_hangouts.db

config = context.config
mxhg_config_path = context.get_x_argument(as_dictionary=True).get("config", "config.yaml")
mxhg_config = Config(mxhg_config_path, None, None)
mxhg_config.load()
config.set_main_option("sqlalchemy.url",
                       mxhg_config.get("appservice.database", "sqlite:///mautrix-hangouts.db"))
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        render_as_batch=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
