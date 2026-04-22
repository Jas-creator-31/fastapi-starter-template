from redis import asyncio as redis
from settings import redis_host, redis_db, redis_port


async def get_redis():
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        db=redis_db,
        decode_responses=True,
    )
    await r.config_set("save", "900 1 300 10 60 10000")
    
    return r
