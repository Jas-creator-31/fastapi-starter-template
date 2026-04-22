from typing import Literal
import logging
import anyio
import anyio.to_thread
from argon2 import PasswordHasher

ph = PasswordHasher()

logger = logging.getLogger(__name__)


async def hash(plain: str) -> str:
    logger.info("hash function triggered")
    return await anyio.to_thread.run_sync(ph.hash, plain)


async def verify_hash(plain: str, hashed: str) -> Literal[True]:
    logger.info("verify_hash function triggered")
    return await anyio.to_thread.run_sync(ph.verify, hashed, plain)
