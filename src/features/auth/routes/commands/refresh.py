from http.client import responses

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from src.core.application.get_services import get_services, Services
from src.core.rate_limiting.limiter import limiter


route = APIRouter()

@route.post("/refresh")
@limiter.limit('30/hour')
async def refresh(
    request: Request,
    service: Services = Depends(get_services)
):
    auth = service.auth
    refresh_token = request.cookies.get("refresh_token")
    tokens = await auth.refresh(refresh_token)
    content = {"status": "success"}
    response = JSONResponse(content=content)
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        max_age=900,
        path="/",
        secure=True,
        samesite="lax",
        httponly=True,
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        max_age=604800,
        path="/",
        secure=True,
        samesite="lax",
        httponly=True,
    )

    return response
