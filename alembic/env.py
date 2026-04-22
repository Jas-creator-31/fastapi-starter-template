import asyncio
from logging.config import fileConfig
from pathlib import Path
from settings import (
    db_username,
    db_secret_key,
    db_host,
    db_port,
    db_name
)
from alembic import context
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
dotenv_path = project_root / ".env"

if not dotenv_path.exists():
    print(f"CRITICAL: .env file not found at {dotenv_path}")
load_dotenv(dotenv_path, override=True)

DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_secret_key}@{db_host}:{db_port}/{db_name}"

print("--- DEBUG: ENV LOADING ---")
print(f"Project Root: {project_root}")
print(f"Connecting as: {db_username} to {db_host}:{db_port}/{db_name}")
print("--------------------------")

from src.db.base import Base  # noqa: E402
from src.db.models.app_users import AppUser  # noqa: E402, F401
from src.db.models.RBAC import Permissions, RolePermissions, Roles, UserRoles  # noqa: E402, F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

print("--- DEBUG 1: REGISTERED TABLES IN PYTHON ---")
print(f"Found: {list(target_metadata.tables.keys())}")
print("--------------------------------------------")

def do_run_migrations(connection: Connection) -> None:
    connection.execute(text("SET search_path TO public"))

    db_name = connection.execute(text("SELECT current_database()")).scalar()
    print(f"--- DEBUG 2: DATABASE CONNECTION SUCCESSFUL: {db_name} ---")

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()
async def run_async_migrations() -> None:
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.begin() as connection:
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"CRITICAL ERROR during connection: {e}")
        raise e
    finally:
        await connectable.dispose()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (for --sql)."""
    url = DATABASE_URL.replace("%", "%%")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
