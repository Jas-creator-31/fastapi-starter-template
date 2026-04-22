from sqlalchemy import Index, Table, Column, ForeignKey
from sqlalchemy.orm import registry
from src.db.base import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id", 
        ForeignKey("app_users.user_id"), 
        primary_key=True, 
    ),
    Column(
        "role_id", 
        ForeignKey("roles.role_id"), 
        primary_key=True, 
    ),

    Index(
        "ix_user_roles_role_user", 
        "role_id", 
        "user_id"
    )
)

class UserRoles:
    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

m = registry()
m.map_imperatively(UserRoles, user_roles)