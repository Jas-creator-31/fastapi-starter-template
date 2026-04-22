import logging

from src.db.models.app_users import AppUser
from src.core.security.hashing_functions import verify_hash

logger = logging.getLogger(__name__)

class User:
    def __init__(self, user: AppUser | None) -> None:
        logger.info(
            "User domain object initialized"
        )
        self.data = user

    async def verify_password(self, password: str):
        logger.info("varify_password triggered")
        if self.data:
            return await verify_hash(password, self.data.password_hash)
