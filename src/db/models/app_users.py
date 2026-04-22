from sqlalchemy import text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.db.base import Base
from uuid import UUID
from datetime import datetime


class AppUser(Base):
    __tablename__ = "app_users"  # type: ignore

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)

    password_hash: Mapped[str] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=text("NULL")
    )
