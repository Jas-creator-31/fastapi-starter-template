from sqlalchemy import Index, Table, Column, ForeignKey
from sqlalchemy.orm import registry
from src.db.base import Base

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        ForeignKey("roles.role_id"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        ForeignKey("permissions.permission_id"),
        primary_key=True,
    ),
    Index("ix_permission_roles_role_permissions", "role_id", "permission_id"),
)

class RolePermissions:
    def __init__(self, role_id, permission_id):
        self.role_id = role_id
        self.permission_id = permission_id


m = registry()
m.map_imperatively(RolePermissions, role_permissions)