from slowapi import Limiter
from slowapi.util import get_remote_address
from settings import settings

url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"

limiter = Limiter(
    key_func=get_remote_address, 
    strategy="moving-window",
    storage_uri=url,
    default_limits=['60/minute'],
    in_memory_fallback_enabled=True
)