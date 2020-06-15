import re
import typing as t

if t.TYPE_CHECKING:
    from mypy_extensions import TypedDict
    from .service_connector import ServiceConnector
    from typing_extensions import Literal

    _NamesAndRolesData = TypedDict('_NamesAndRolesData', {
        'context_memberships_url': str,
    }, total=False)
    _Member = TypedDict('_Member', {
        'name': str,
        'status': Literal['Active', 'Inactive', 'Deleted'],
        'picture': str,
        'given_name': str,
        'family_name': str,
        'middle_name': str,
        'email': str,
        'user_id': str,
        'lis_person_sourcedid': str,
        'roles': t.List[str],
        'message': t.Union[t.List[t.Dict[str, object]], t.Dict[str, object]],
        'lti11_legacy_user_id': t.Optional[str],
    }, total=False)


class NamesRolesProvisioningService(object):
    _service_connector = None  # type: ServiceConnector
    _service_data = None  # type: _NamesAndRolesData

    def __init__(self, service_connector, service_data):
        # type: (ServiceConnector, _NamesAndRolesData) -> None
        self._service_connector = service_connector
        self._service_data = service_data

    def get_members(self):
        # type: () -> t.List[_Member]
        members = []  # type: t.List[_Member]
        next_page = self._service_data['context_memberships_url']  # type: t.Union[Literal[False], str]

        while next_page:
            page = self._service_connector.make_service_request(
                ['https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly'],
                next_page,  # type: ignore
                accept='application/vnd.ims.lti-nrps.v2.membershipcontainer+json'
            )

            members.extend(t.cast(t.Any, page.get('body', {})).get('members', []))

            next_page = False
            link_header = page.get('headers', {}).get('link', '')
            if link_header:
                match = re.search(r'<([^>]*)>;\s*rel="next"', link_header.replace('\n', ' ').lower().strip())
                if match:
                    next_page = match.group(1)

        return members
