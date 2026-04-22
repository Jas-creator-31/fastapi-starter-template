from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.features.auth.types import token_type
class LoginPayload(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(
        from_attributes=True
    )

class UserAgentInfo(BaseModel):
    browser: Optional[str]
    os: Optional[str]
    device: Optional[str]
    is_mobile: Optional[bool]

class TokenServiceReturn(BaseModel):
    sid: UUID
    access_token: str
    refresh_token: str
    hashed_refresh_token: str

class Token(BaseModel):
    sub: UUID
    iat: datetime
    exp: datetime
    type: token_type
    sid: UUID
    iss: str
    aud: str
    jti: UUID

class AsLogin(BaseModel):
    access_token: str
    refresh_token: str