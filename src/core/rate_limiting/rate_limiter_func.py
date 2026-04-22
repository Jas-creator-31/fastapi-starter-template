from slowapi.util import get_remote_address
from fastapi import Request
from src.features.auth.services.token_service import TokenService

async def rate_limiter_func(request: Request):
    if request.url.path.startswith("/__radar"):
        return None
    token = request.cookies.get("access_token")
    if not token:
        return get_remote_address(request) # use get_ipaddr if using a reverse proxy
    
    token_service: TokenService = request.app.state.token_service
    decoded_token = await token_service.verify_token(token)
    user_id = decoded_token.sub
    return user_id