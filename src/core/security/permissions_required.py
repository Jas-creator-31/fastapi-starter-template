from functools import wraps
from src.core.context.user_context import user_context
from src.core.errors.domain_errors import NotHasPermissionError

def permissions_required(perm_slang: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            context = user_context.get()
            if perm_slang not in context.role_permissions:
                raise NotHasPermissionError
            return await func(*args, **kwargs)
        return wrapper
    return decorator