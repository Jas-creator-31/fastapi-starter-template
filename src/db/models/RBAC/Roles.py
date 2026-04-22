from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.db.base import Base
from uuid import UUID


class Roles(Base):
    __tablename__ = "roles"  # type: ignore

    role_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    name: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        nullable=False,
    )
