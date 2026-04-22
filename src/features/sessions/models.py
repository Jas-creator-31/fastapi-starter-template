import datetime
from uuid import UUID

from pydantic import BaseModel


class RedisSessionValueType(BaseModel):
    user_id: UUID
    user_roles: list[str]
    user_permissions: list[str]
    refresh_hash: str
    absolute_expiry: datetime.datetime
    ip_address: str
    device_info: str
    browser: str
    os: str


class RedisSessionsSeviceReturn(BaseModel):
    access_token: str
    refresh_token: str
