from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.db.base import Base
from uuid import UUID


class Permissions(Base):
    __tablename__ = "permissions"  # type: ignore

    permission_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)

    permission_slang: Mapped[str] = mapped_column(
        String(30),  # basic limit can be changed for application specific needs
        nullable=False,
        index=True,
        unique=True,
    )

    description: Mapped[str] = mapped_column(String(200), nullable=False)
