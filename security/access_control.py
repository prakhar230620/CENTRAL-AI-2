import logging
from enum import Enum, auto

class Role(Enum):
    ADMIN = auto()
    MANAGER = auto()
    USER = auto()

class Permission(Enum):
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    EXECUTE = auto()

class AccessControl:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.role_permissions = {
            Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE},
            Role.MANAGER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
            Role.USER: {Permission.READ, Permission.EXECUTE}
        }
        self.user_roles = {}

    def assign_role(self, user_id, role):
        if not isinstance(role, Role):
            raise ValueError("Invalid role")
        self.user_roles[user_id] = role
        self.logger.info(f"Assigned role {role.name} to user {user_id}")

    def get_user_role(self, user_id):
        return self.user_roles.get(user_id, Role.USER)

    def check_permission(self, user_id, permission):
        if not isinstance(permission, Permission):
            raise ValueError("Invalid permission")
        user_role = self.get_user_role(user_id)
        has_permission = permission in self.role_permissions[user_role]
        self.logger.info(f"User {user_id} {'has' if has_permission else 'does not have'} {permission.name} permission")
        return has_permission

    def grant_permission(self, role, permission):
        if not isinstance(role, Role) or not isinstance(permission, Permission):
            raise ValueError("Invalid role or permission")
        self.role_permissions[role].add(permission)
        self.logger.info(f"Granted {permission.name} permission to role {role.name}")

    def revoke_permission(self, role, permission):
        if not isinstance(role, Role) or not isinstance(permission, Permission):
            raise ValueError("Invalid role or permission")
        self.role_permissions[role].discard(permission)
        self.logger.info(f"Revoked {permission.name} permission from role {role.name}")