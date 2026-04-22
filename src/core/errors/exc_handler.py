from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging

from src.core.errors.domain_errors import (
    AuthenticationError,
    ExpiredJwtSignatureError,
    InvalidJwtSignatureError,
    InvalidJwtTokenError,
    NotHasPermissionError,
    InternalServerError
)

logger = logging.getLogger(__name__)

def exception_handler(app: FastAPI) -> None:

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global error caught: {exc}", exc_info=True) 

        return JSONResponse(
            status_code=500,
            content={
                "message": "An internal server error occurred.",
                "detail": str(exc) if app.debug else None # Hide details in production
            }
        )
    @app.exception_handler(AuthenticationError)
    async def authentication_error(
        request: Request, exc: AuthenticationError
    ) -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    @app.exception_handler(ExpiredJwtSignatureError)
    async def expired_jwt_signature_error(
        request: Request, exc: ExpiredJwtSignatureError
    ) -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=
            """
            The accesstoken has expired.
            Please use your refresh token to obtain a new one
            """,
        )

    @app.exception_handler(InvalidJwtSignatureError)
    async def invalid_jwt_signature_error(
        request: Request, exc: InvalidJwtSignatureError
    ) -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="""
                The access token provided is invalid or malformed"
            """,
        )

    @app.exception_handler(InvalidJwtTokenError)
    async def Invalid_jwt_token_error(
        request: Request, exc: InvalidJwtTokenError
    ) -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=
            """
            The access token provided is invalid or malformed
            """,
        )

    @app.exception_handler(NotHasPermissionError)
    async def not_has_permission_error(
        request: Request, exc: NotHasPermissionError
    ) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="insufficient_permission",
        )

    app.exception_handler(InternalServerError)
    async def internal_server_error(
        request: Request, exc: InternalServerError
    ) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error has occurred",
        )

    app.add_exception_handler(
        RateLimitExceeded,
        _rate_limit_exceeded_handler,  # type: ignore
    )
