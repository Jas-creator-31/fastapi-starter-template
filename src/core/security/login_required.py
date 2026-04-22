from functools import wraps
from fastapi.responses import RedirectResponse
from src.core.context.user_context import user_context

def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        context = user_context.get()
        if not context.user_id:
            RedirectResponse("/auth/refresh")
        return await func(*args, **kwargs)
    return wrapper
