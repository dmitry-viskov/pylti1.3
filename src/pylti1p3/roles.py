from abc import ABCMeta
import typing as t
import typing_extensions as te


class RoleType:
    SYSTEM: te.Final = "system"
    INSTITUTION: te.Final = "institution"
    CONTEXT: te.Final = "membership"


class AbstractRole:
    __metaclass__ = ABCMeta
    _base_prefix: str = "http://purl.imsglobal.org/vocab/lis/v2"
    _role_types = [RoleType.SYSTEM, RoleType.INSTITUTION, RoleType.CONTEXT]
    _jwt_roles: t.List[str] = []
    _common_roles: t.Optional[t.Tuple] = None
    _system_roles: t.Optional[t.Tuple] = None
    _institution_roles: t.Optional[t.Tuple] = None
    _context_roles: t.Optional[t.Tuple] = None

    def __init__(self, jwt_body):
        self._jwt_roles = jwt_body.get(
            "https://purl.imsglobal.org/spec/lti/claim/roles", []
        )

    def check(self) -> bool:
        for role_str in self._jwt_roles:
            role_name, role_type = self.parse_role_str(role_str)
            res = self._check_access(role_name, role_type)
            if res:
                return True
        return False

    def _check_access(self, role_name: str, role_type: t.Optional[str] = None):
        return bool(
            (
                self._system_roles
                and role_type == RoleType.SYSTEM
                and role_name in self._system_roles
            )
            or (
                self._institution_roles
                and role_type == RoleType.INSTITUTION
                and role_name in self._institution_roles
            )
            or (
                self._context_roles
                and role_type == RoleType.CONTEXT
                and role_name in self._context_roles
            )
            or (
                self._common_roles
                and role_type is None
                and role_name in self._common_roles
            )
        )

    def parse_role_str(self, role_str: str) -> t.Tuple[str, t.Optional[str]]:
        if role_str.startswith(self._base_prefix):
            role = role_str[len(self._base_prefix) :]
            role_parts = role.split("/")
            role_name_parts = role.split("#")

            if len(role_parts) > 1 and len(role_name_parts) > 1:
                role_type = role_parts[1]
                role_name = role_name_parts[1]
                if role_type in self._role_types:
                    return role_name, role_type
                return role_name, None
        return role_str, None


class StaffRole(AbstractRole):
    _system_roles = ("Administrator", "SysAdmin")
    _institution_roles = ("Faculty", "SysAdmin", "Staff", "Instructor")


class StudentRole(AbstractRole):
    _common_roles = ("Learner", "Member", "User")
    _system_roles = ("User",)
    _institution_roles = ("Student", "Learner", "Member", "ProspectiveStudent", "User")
    _context_roles = ("Learner", "Member")


class TeacherRole(AbstractRole):
    _common_roles = ("Instructor", "Administrator")
    _context_roles = ("Instructor", "Administrator")


class TeachingAssistantRole(AbstractRole):
    _context_roles = ("TeachingAssistant",)


class DesignerRole(AbstractRole):
    _common_roles = ("ContentDeveloper",)
    _context_roles = ("ContentDeveloper",)


class ObserverRole(AbstractRole):
    _common_roles = ("Mentor",)
    _context_roles = ("Mentor",)


class TransientRole(AbstractRole):
    _common_roles = ("Transient",)
    _system_roles = ("Transient",)
    _institution_roles = ("Transient",)
    _context_roles = ("Transient",)
