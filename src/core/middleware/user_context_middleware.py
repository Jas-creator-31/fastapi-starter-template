from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
from fastapi import Request
from redis.asyncio import Redis
from src.core.context.user_context import (
    UserContext,
    user_context,
)
from src.features.auth.services.token_service import (
    TokenService,
)

logger = logging.getLogger(__name__)

class UserContextMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        token_service: TokenService = (
            request.app.state.token_service
        )
        redis: Redis = request.app.state.redis
        token = request.cookies.get("access_token")
        if not token:
            context = UserContext(
                user_id=None,
                user_roles=[],
                role_permissions=[],
            )
        else:
            try:

                b_token = token.encode("utf-8")
                decoded_token = await token_service.decode_token(
                    b_token
                )
                value = await redis.hgetall(f"auth:session:{str(decoded_token.sid)}")  # type: ignore

                if not value:
                    # Handle expired/missing session safely
                    context = UserContext(
                        user_id=None,
                        user_roles=[],
                        role_permissions=[],
                    )
                else:
                    # Use .get() to avoid KeyError and json.loads() to convert string back to list
                    context = UserContext(
                        user_id=decoded_token.sub,
                        user_roles=json.loads(
                            value.get(
                                "user_roles", "[]"
                            )
                        ),
                        role_permissions=json.loads(
                            value.get(
                                "role_permissions",
                                "[]",
                            )
                        ),
                    )
            except Exception as e:
                logger.error(
                    f"Auth middleware failed: {e}"
                )
                context = UserContext(
                    user_id=None,
                    user_roles=[],
                    role_permissions=[],
                )
        context_token = user_context.set(context)
        try:
            return await call_next(request)

        finally:
            user_context.reset(context_token)
