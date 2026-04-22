from fastapi import Depends, Request
from pydantic import BaseModel, ConfigDict
from src.core.application.get_repos import Repos, get_repos
from src.features.auth.services.auth_service import AuthService
from src.features.auth.services.token_service import TokenService
from src.features.RBAC.access_ctl_service import AccessCtlService
from src.features.sessions.sessions_service import SessionsService


class Services(BaseModel):
    auth: AuthService
    token: TokenService
    sessions: SessionsService
    access_ctl: AccessCtlService

    model_config=ConfigDict(
        arbitrary_types_allowed=True
    )



async def get_services(req: Request, repos: Repos = Depends(get_repos)):
    token = req.app.state.token_service
    sessions = SessionsService(repos.sessions, token, repos.access_ctl)
    auth = AuthService(repos.user, sessions, token)
    access_ctl = AccessCtlService(repos.access_ctl)
    return Services(auth=auth, token=token, sessions=sessions, access_ctl=access_ctl)
