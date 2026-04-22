from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.features.auth.services.token_service import TokenService
from src.infra.redis.client import get_redis
from src.core.application.cache_key_builder import cache_key_builder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await get_redis()
    token = TokenService()
    FastAPICache.init(RedisBackend(redis), prefix="cache", key_builder=cache_key_builder)
    if hasattr(app.state, "radar"):
        app.state.radar.create_tables()
    app.state.redis = redis
    app.state.token_service = token
    yield
