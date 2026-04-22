from slowapi import Limiter
from slowapi.util import get_remote_address
from settings import redis_host, redis_db, redis_port

url = f"redis://{redis_host}:{redis_port}/{redis_db}"

limiter = Limiter(
    key_func=get_remote_address, 
    strategy="moving-window",
    storage_uri=url,
    default_limits=['60/minute'],
    in_memory_fallback_enabled=True
)