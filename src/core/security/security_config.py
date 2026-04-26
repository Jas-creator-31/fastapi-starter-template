from guard import SecurityConfig
from settings import settings

url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"

allowed_origins = [
    "https://localhost",
    "https://192.168.31.190",
]

exclude_paths_for_rate_limiting = [
    "/__radar/",
    "/__radar",
    "/docs"
]

security_config = SecurityConfig(
    enable_rate_limiting=True,
    rate_limit=100,
    rate_limit_window=60,
    exclude_paths=exclude_paths_for_rate_limiting,
    enable_redis=True,
    redis_url=url,
    redis_prefix="guard",
    enable_ip_banning=True,
    auto_ban_threshold=5,
    auto_ban_duration=86400,
    custom_log_file="security.log",
    enforce_https=True,
    enable_cors=True,
    cors_allow_origins=allowed_origins,
    cors_allow_methods=["GET", "POST"],
    cors_allow_headers=["*"],
    cors_allow_credentials=True,
    cors_max_age=600,
    block_cloud_providers={"AWS", "Azure"},
)
