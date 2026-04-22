from datetime import datetime, timedelta, timezone
import logging
from uuid import uuid4
from src.core.context.request_context import request_metadata_context
from src.features.auth.services.token_service import TokenService
from src.features.sessions.models import (
    RedisSessionsSeviceReturn,
    RedisSessionValueType,
)
from src.features.sessions.sessions_repo import SessionsRepo

logger = logging.getLogger(__name__)

class SessionsService:
    def __init__(self, sessions_repo, token_service, access_ctl_repo) -> None:
        logger.info("SessionsService initialized")
        self.sessions_repo: SessionsRepo = sessions_repo
        self.token_service: TokenService = token_service
        self.access_ctl_repo = access_ctl_repo

    async def _create_redis_value(self, user_id, refresh_hash, roles, permissions):
        logger.info("_create_redis_value method started")
        request_metadata = request_metadata_context.get()
        now = datetime.now(timezone.utc)
        redis_value = RedisSessionValueType(
            user_id=user_id,
            refresh_hash=refresh_hash,
            absolute_expiry=now + timedelta(days=30),
            user_roles=roles,
            user_permissions=permissions,
            ip_address=request_metadata.client_ip,
            browser=request_metadata.user_agent.browser,  # type: ignore
            device_info=request_metadata.user_agent.device,  # type: ignore
            os=request_metadata.user_agent.os,  # type: ignore
        )
        logger.info("_create_redis_value method started")
        return redis_value

    async def create_session(self, user_id):
        logger.info("create_session method started")
        sid = uuid4()
        tokens = await self.token_service.issue_token_pair(user_id, "create", sid)
        roles, permissions = await self.access_ctl_repo.get_roles_and_permissions(
            user_id
        )
        redis_value = await self._create_redis_value(
            user_id,
            tokens.hashed_refresh_token,
            roles,
            permissions,
        )
        (
            await self.sessions_repo.set_token(
                sid,
                redis_value,
            )
        )
        logger.info("create_session method ended")
        return tokens.access_token, tokens.refresh_token

    async def refresh_session(self, user_id, sid):
        logger.info("refresh_session method started")
        tokens = await self.token_service.issue_token_pair(user_id, "refresh", sid)
        await self.sessions_repo.update_refresh_hash(sid, tokens.hashed_refresh_token)
        logger.info("refresh_session method ended")
        return RedisSessionsSeviceReturn(
            access_token=tokens.access_token, refresh_token=tokens.refresh_token
        )
