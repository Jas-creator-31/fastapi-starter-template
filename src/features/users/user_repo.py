import logging

from pydantic import EmailStr
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.app_users import AppUser
from src.features.users.user import User

logger = logging.getLogger(__name__)

class UserRepo:
    def __init__(self, db: AsyncSession) -> None:
        logger.info("UserRepo repo initialized")
        self.db = db

    async def exist(self, email: EmailStr):
        logger.info("exist methon started")
        stmt = (
            select(AppUser)
            .where(
                and_(
                        AppUser.email == email,
                        AppUser.deleted_at == None  # noqa: E711
                    )
                )
            )
        res = await self.db.scalars(stmt)
        user = res.first()
        logger.info("exist methon ended")
        return User(
            user
        )

    async def get_user(self, user_id):
        logger.info("get_user methon started")
        stmt = (
            select(AppUser)
            .where(AppUser.user_id == user_id)
        )
        res = await self.db.scalars(stmt)
        user = res.one()
        logger.info("get_user methon ended")
        return User(
            user
        )
