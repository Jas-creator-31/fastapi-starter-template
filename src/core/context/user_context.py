from contextvars import ContextVar
from uuid import UUID
from pydantic import BaseModel

class UserContext(BaseModel):
    user_id: UUID | None
    user_roles: list = []
    role_permissions: list = []


user_context: ContextVar[UserContext] = ContextVar("user")
