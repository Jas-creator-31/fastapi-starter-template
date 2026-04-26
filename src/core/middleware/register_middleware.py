import logging
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from slowapi.middleware import SlowAPIMiddleware
from starlette_csrf.middleware import CSRFMiddleware
from settings import settings
from src.core.middleware.request_context_middleware import RequestContextMiddleware
from src.core.middleware.user_context_middleware import UserContextMiddleware
from guard import SecurityMiddleware

from src.core.security.security_config import security_config

allowed_hosts = [
    "localhost",
    "jashanpreet.me",
    "*.jashanpreet.me",
    "*.ngrok-free.dev",
    "0.0.0.0"
]

logger = logging.getLogger(__name__)

def register_middleware(app: FastAPI):

    app.add_middleware(
        UserContextMiddleware
    )

    app.add_middleware(
        RequestContextMiddleware
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
        compresslevel=5  
    )
    app.add_middleware(
        CorrelationIdMiddleware
    )
    app.add_middleware(
        SlowAPIMiddleware
    )
    app.add_middleware(
        CSRFMiddleware,
        secret=settings.csrf_key.get_secret_value(),
        cookie_name="fastapi-csrf-token",
        cookie_secure=True,
        cookie_httponly=True,
        cookie_samesite="lax",
        header_name="X-CSRF-Token",
    )
    app.add_middleware(
        SecurityMiddleware,
        config=security_config
    )
    app.add_middleware(ProxyHeadersMiddleware)
