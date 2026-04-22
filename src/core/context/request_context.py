from contextvars import ContextVar
from pydantic import BaseModel
from src.features.auth.models import UserAgentInfo


class RequestContext(BaseModel):
    client_ip: str
    user_agent: UserAgentInfo


request_metadata_context: ContextVar[RequestContext] = ContextVar("request_metadata")
