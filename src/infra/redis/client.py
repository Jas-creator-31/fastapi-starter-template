from redis import asyncio as redis
from settings import settings


async def get_redis():
    r = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True,
    )
    await r.config_set("save", "900 1 300 10 60 10000")
    
    return r
