from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.app_users import AppUser
from src.db.models.RBAC.Permissions import Permissions
from src.db.models.RBAC.RolePermissions import RolePermissions
from src.db.models.RBAC.Roles import Roles
from src.db.models.RBAC.UserRoles import UserRoles


class AccessCtlRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def has_permission(self, user_id, permission_slang):
        subq = (
            select(AppUser)
            .where(AppUser.user_id == user_id)
            .join(UserRoles)
            .join(RolePermissions)
            .join(Permissions, Permissions.permission_slang == permission_slang)
        )
        stmt = subq.exists().select()
        res = await self.db.execute(stmt)
        result = res.scalar()
        return result

    async def get_roles_and_permissions(self, user_id):
        roles_stmt = (
            select(Roles.name)
            .select_from(UserRoles)
            .join(Roles, Roles.role_id == UserRoles.role_id)  # type: ignore
            .where(UserRoles.user_id == user_id)  # type: ignore
        )
        roles_res = await self.db.scalars(roles_stmt)
        roles = list(dict.fromkeys(roles_res.all()))

        perms_stmt = (
            select(Permissions.permission_slang)
            .select_from(UserRoles)
            .join(RolePermissions, RolePermissions.role_id == UserRoles.role_id)  # type: ignore
            .join(
                Permissions,
                Permissions.permission_id == RolePermissions.permission_id,  # type: ignore
            )
            .where(UserRoles.user_id == user_id)  # type: ignore
        )
        perms_res = await self.db.scalars(perms_stmt)
        permissions = list(dict.fromkeys(perms_res.all()))

        return roles, permissions
