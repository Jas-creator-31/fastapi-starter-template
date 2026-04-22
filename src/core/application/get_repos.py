from fastapi import Depends, Request
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.deps import get_async_db
from src.features.RBAC.access_ctl_repo import AccessCtlRepo
from src.features.sessions.sessions_repo import SessionsRepo
from src.features.users.user_repo import UserRepo


class Repos(BaseModel):
    user: UserRepo
    sessions: SessionsRepo
    access_ctl: AccessCtlRepo
    
    model_config=ConfigDict(
        arbitrary_types_allowed=True
    )


async def get_repos(
    req: Request,
    db: AsyncSession = Depends(get_async_db),
):
    redis = req.app.state.redis
    user = UserRepo(db)
    sessions = SessionsRepo(redis)
    access_ctl = AccessCtlRepo(db)

    return Repos(user=user, sessions=sessions, access_ctl=access_ctl)
