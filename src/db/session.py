import logging

from sqlalchemy import create_engine
from settings import settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.exc import SQLAlchemyError, DatabaseError
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio.engine import (
    AsyncEngine,
)
from src.core.errors.domain_errors import (
    InternalServerError,
)

logger = logging.getLogger(__name__)


try:
    logger.info("trying to create a database URL")
    database_url = URL.create(
        drivername=settings.db_driver,
        username=settings.db_username,
        password=settings.db_secret_key.get_secret_value(),
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )
except Exception as e:
    logger.exception(
        f"error: {e} occurred while trying to create a database URL"
    )
    raise InternalServerError


try:
    logger.info("trying to create a database engine")
    engine: AsyncEngine = create_async_engine(
        database_url
    )
    radar_engine = create_engine("sqlite:///radar_metrics.settings.db")
    logger.info("database engine successfully created")
except SQLAlchemyError as e:
    logger.exception(
        f"error: {e} occurred while trying to create a database engine"
    )
    raise InternalServerError

try:
    logger.info("trying to create a database session")
    AsyncSessionLocal: async_sessionmaker[
        AsyncSession
    ] = async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    logger.info("database session successfully created")
except DatabaseError as e:
    logger.exception(f"error: {e} occurred while trying to create a database session")
    raise InternalServerError