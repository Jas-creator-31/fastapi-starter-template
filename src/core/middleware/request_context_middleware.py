from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
import logging
from fastapi import Request
import logging
from fastapi import Request
from user_agents import parse
from src.core.context.request_context import RequestContext, request_metadata_context
from src.features.auth.models import UserAgentInfo

logger = logging.getLogger(__name__)

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("user-agent", "")
        raw_ua = parse(user_agent)
        client_ip: str = request.headers.get("x-forwarded-for", request.client.host)  # type: ignore

        ua = UserAgentInfo(
            browser=raw_ua.browser.family,
            device=raw_ua.device.family,
            os=raw_ua.os.family,
            is_mobile=raw_ua.is_mobile,
        )

        new_metadata = RequestContext(client_ip=client_ip, user_agent=ua)
        token = request_metadata_context.set(new_metadata)

        try:
            return await call_next(request)

        finally:
            request_metadata_context.reset(token)