import logging
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from asgi_correlation_id import CorrelationIdMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from slowapi.middleware import SlowAPIMiddleware
from starlette_csrf.middleware import CSRFMiddleware
from redis.asyncio import Redis
from user_agents import parse
from src.core.context.request_context import RequestContext, request_metadata_context
from src.core.context.user_context import UserContext, user_context
from src.features.auth.models import UserAgentInfo
from src.features.auth.services.token_service import TokenService
from settings import settings
from src.core.middleware.request_context_middleware import RequestContextMiddleware
from src.core.middleware.user_context_middleware import UserContextMiddleware

allowed_origins = [
        "https://ledgeless-solvolytic-jesenia.ngrok-free.dev",
        "https://localhost",
        "https://192.168.31.190",
        "https://tijuana-unsymbolical-miss.ngrok-free.dev",
        "https://jashanpreet.me",
]
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
    app.add_middleware(ProxyHeadersMiddleware)
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=allowed_hosts
    )
    app.add_middleware(HTTPSRedirectMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,  # List of allowed origins
        allow_credentials=True,  # Allow cookies/authorization headers (requires specific origins)
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Allow all HTTP request headers
    )
  