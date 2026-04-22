from fastapi import APIRouter, Depends, Response, Request
from fastapi.responses import JSONResponse
from src.features.auth.models import LoginPayload
from src.core.rate_limiting.limiter import limiter
from src.core.application.get_services import get_services, Services
import logging

route = APIRouter()

logger = logging.getLogger(__name__)

@route.post('/login')
@limiter.limit('5/minute')
async def login(
	request: Request,
    payload: LoginPayload,
	service: Services = Depends(get_services)
    
):

    logger.info("login route started")
    auth = service.auth

    as_login = await auth.login(payload)

    content = {"status": "success"}
    response = JSONResponse(content=content)

    response.set_cookie(
        key="access_token",
        value=as_login.access_token,
        max_age=900,
        path="/",
        secure=True,
        samesite="lax",
        httponly=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=as_login.refresh_token,
        max_age=604800,
        path="/",
        secure=True,
        samesite="lax",
        httponly=True,
    )

    logger.info("login route ended")
    return response
