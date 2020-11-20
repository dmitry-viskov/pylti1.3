from abc import ABCMeta
import typing as t

if t.TYPE_CHECKING:
    from typing_extensions import Final


class RoleType(object):
    SYSTEM = 'system'  # type: Final
    INSTITUTION = 'institution'  # type: Final
    CONTEXT = 'membership'  # type: Final


class AbstractRole(object):
    __metaclass__ = ABCMeta
    _base_prefix = 'http://purl.imsglobal.org/vocab/lis/v2'  # type: str
    _role_types = [RoleType.SYSTEM, RoleType.INSTITUTION, RoleType.CONTEXT]  # type: list
    _jwt_roles = []  # type: list
    _common_roles = None  # type: t.Optional[tuple]
    _system_roles = None  # type: t.Optional[tuple]
    _institution_roles = None  # type: t.Optional[tuple]
    _context_roles = None  # type: t.Optional[tuple]

    def __init__(self, jwt_body):
        self._jwt_roles = jwt_body.get('https://purl.imsglobal.org/spec/lti/claim/roles', [])

    def check(self):
        # type: () -> bool
        for role_str in self._jwt_roles:
            role_name, role_type = self.parse_role_str(role_str)
            res = self._check_access(role_name, role_type)
            if res:
                return True
        return False

    def _check_access(self, role_name, role_type=None):
        # type: (str, t.Optional[str]) -> bool
        return bool((self._system_roles and role_type == RoleType.SYSTEM and role_name in self._system_roles)
                    or (self._institution_roles and role_type == RoleType.INSTITUTION
                        and role_name in self._institution_roles)
                    or (self._context_roles and role_type == RoleType.CONTEXT and role_name in self._context_roles)
                    or (self._common_roles and role_type is None and role_name in self._common_roles))

    def parse_role_str(self, role_str):
        # type: (str) -> t.Tuple[str, t.Optional[str]]
        if role_str.startswith(self._base_prefix):
            role = role_str[len(self._base_prefix):]
            role_parts = role.split('/')
            role_name_parts = role.split('#')

            if len(role_parts) > 1 and len(role_name_parts) > 1:
                role_type = role_parts[1]
                role_name = role_name_parts[1]
                if role_type in self._role_types:
                    return role_name, role_type
                return role_name, None
        return role_str, None


class StaffRole(AbstractRole):
    _system_roles = ('Administrator', 'SysAdmin')  # type: tuple
    _institution_roles = ('Faculty', 'SysAdmin', 'Staff', 'Instructor')  # type: tuple


class StudentRole(AbstractRole):
    _common_roles = ('Learner', 'Member', 'User')  # type: tuple
    _system_roles = ('User',)  # type: tuple
    _institution_roles = ('Student', 'Learner', 'Member', 'ProspectiveStudent', 'User')  # type: tuple
    _context_roles = ('Learner', 'Member')  # type: tuple


class TeacherRole(AbstractRole):
    _common_roles = ('Instructor', 'Administrator')  # type: tuple
    _context_roles = ('Instructor', 'Administrator')  # type: tuple


class TeachingAssistantRole(AbstractRole):
    _context_roles = ('TeachingAssistant',)  # type: tuple


class DesignerRole(AbstractRole):
    _common_roles = ('ContentDeveloper',)  # type: tuple
    _context_roles = ('ContentDeveloper',)  # type: tuple


class ObserverRole(AbstractRole):
    _common_roles = ('Mentor',)  # type: tuple
    _context_roles = ('Mentor',)  # type: tuple


class TransientRole(AbstractRole):
    _common_roles = ('Transient',)  # type: tuple
    _system_roles = ('Transient',)  # type: tuple
    _institution_roles = ('Transient',)  # type: tuple
    _context_roles = ('Transient',)  # type: tuple
