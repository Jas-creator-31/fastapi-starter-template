from src.features.RBAC.access_ctl_repo import AccessCtlRepo

class AccessCtlService:
    def __init__(self, repo) -> None:
        self.repo: AccessCtlRepo = repo
    
    async def has_permission(self, user_id, permission_slang):
        res = await self.repo.has_permission(user_id, permission_slang)
        return res

