import json
import logging
from redis.asyncio import Redis
from src.features.sessions.models import RedisSessionValueType

logger = logging.getLogger(__name__)

class SessionsRepo:

    def __init__(self, redis) -> None:
        logger.info("SessionsRepo repo initialized")
        self.redis: Redis = redis

    async def set_token(self, session_id, value: RedisSessionValueType):
        logger.info("set_token method started")
        raw_data = value.model_dump(mode="json")
    
        value_to_map = {
            k: (json.dumps(v) if isinstance(v, (list, dict)) else v)
            for k, v in raw_data.items()
        }

        pipe = await self.redis.pipeline(transaction=True)
        pipe.hset(f"auth:session:{session_id}", mapping=value_to_map)
        pipe.expire(f"auth:session:{session_id}", 604800)
        await pipe.execute()
        logger.info("set_token method ended")
    async def get_refresh_token(self, session_id):
        logger.info("set_token method triggered")
        return await self.redis.hget(f"auth:session:{session_id}", "refresh_hash") # type: ignore

    async def update_refresh_hash(self, session_id, new_refresh_hash):
        logger.info("update_refresh_hash method started")
        pipe = await self.redis.pipeline(transaction=True)
        pipe.hset(f"auth:session:{session_id}", "refresh_hash", new_refresh_hash)
        pipe.expire(f"auth:session:{session_id}", 604800)
        await pipe.execute()
        logger.info("update_refresh_hash method ended")
