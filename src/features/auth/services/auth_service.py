from src.core.errors.domain_errors import (
    AuthenticationError,
)
from src.features.auth.models import LoginPayload
from src.features.auth.services.token_service import (
    TokenService,
)
from src.features.sessions.sessions_service import (
    SessionsService,
)
from src.features.users.user_repo import UserRepo
import logging
from src.features.auth.models import AsLogin

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        user_repo,
        sessions_service,
        token_service,
    ):
        logger.info(
            "AuthService service initialized"
        )
        self.user_repo: UserRepo = user_repo
        self.sessions_service: SessionsService = (
            sessions_service
        )
        self.token_service: TokenService = (
            token_service
        )

    async def login(self, payload: LoginPayload):
        logger.info("login method started")
        user_domain = await self.user_repo.exist(
            payload.email
        )
        if not user_domain.data:
            logger.info(
                "user_domain.data is None"
            )
            raise AuthenticationError
        if not await user_domain.verify_password(
            payload.password
        ):
            logger.info(
                "user_domain.varify_password not match"
            )
            raise AuthenticationError
        (access_token, refresh_token) = (
            await self.sessions_service.create_session(
                user_domain.data.user_id
            )
        )
        logger.info("login method ended")
        return AsLogin(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token):
        logger.info("refresh method started")
        decoded_refresh_token = (
            await self.token_service.verify_token(
                refresh_token
            )
        )
        sid = decoded_refresh_token.sid
        user_id = decoded_refresh_token.sub
        logger.info("ss")
        tokens = await self.sessions_service.refresh_session(
            user_id, sid
        )
        logger.info("refresh method ended")
        return tokens
