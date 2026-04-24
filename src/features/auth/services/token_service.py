from datetime import datetime, timedelta, timezone
import logging
from uuid import UUID, uuid4
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)

from settings import settings
from src.core.errors.domain_errors import (
    ExpiredJwtSignatureError,
    InvalidJwtSignatureError,
    InvalidJwtTokenError,
)
from src.core.security.hashing_functions import (
    hash,
)
from src.features.auth.models import (
    Token,
    TokenServiceReturn,
)
from src.features.auth.types import (
    action_type,
    token_type,
)

logger = logging.getLogger(__name__)

class TokenService:
    def __init__(self) -> None:
        pass

    async def _create_token_payload(
        self, user_id, sid, type: token_type
    ):
        logger.info("creating token payload")
        now = datetime.now(timezone.utc)

        exp_time: int = (
            900 if type == "access" else 604800
        )

        token_payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now
            + timedelta(seconds=exp_time),
            "type": type,
            "sid": str(sid),
            "iss": settings.self_url,
            "aud": settings.self_url,
            "jti": str(uuid4()),
        }

        return token_payload

    async def issue_token_pair(
        self,
        user_id,
        action: action_type,
        sid: UUID,
    ):

        access = await self._create_token_payload(
            user_id, sid, "access"
        )
        refresh = (
            await self._create_token_payload(
                user_id, sid, "refresh"
            )
        )

        access_token = jwt.encode(
            access, settings.jwt_secret.get_secret_value(), settings.jwt_algorithm
        )
        refresh_token = jwt.encode(
            refresh, settings.jwt_secret.get_secret_value(), settings.jwt_algorithm
        )

        hashed_refresh_token = await hash(
            refresh_token
        )

        return TokenServiceReturn(
            sid=sid,  # type: ignore
            access_token=access_token,
            refresh_token=refresh_token,
            hashed_refresh_token=hashed_refresh_token,
        )

    async def verify_token(self, token):

        try:
            decoded_token: Token = await self.decode_token(token)  # type: ignore

            return decoded_token
        except ExpiredSignatureError:
            raise ExpiredJwtSignatureError
        except InvalidSignatureError:
            raise InvalidJwtSignatureError
        except InvalidTokenError:
            raise InvalidJwtTokenError

    async def decode_token(self, token):
        decoded_token = jwt.decode(
            token, 
            settings.jwt_secret.get_secret_value(), 
            algorithms=settings.jwt_algorithm,
            audience=settings.self_url
        )  # type: ignore
        return Token(**decoded_token)
