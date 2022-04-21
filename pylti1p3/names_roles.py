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

    def get_nrps_data(self, members_url=None):
        if not members_url:
            members_url = self._service_data['context_memberships_url']

        data = self._service_connector.make_service_request(
            ['https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly'],
            members_url,
            accept='application/vnd.ims.lti-nrps.v2.membershipcontainer+json',
        )
        return data

    def get_members_page(self, members_url=None):
        # type: (t.Optional[str]) -> t.Tuple[list, t.Optional[str]]
        """
        Get one page with the users.

        :param members_url: LTI platform's URL (optional)
        :return: tuple in format: (list with users, next page url)
        """
        data = self.get_nrps_data(members_url=members_url)
        data_body = t.cast(t.Any, data.get('body', {}))
        return data_body.get('members', []), data['next_page_url']

    def get_members(self):
        # type: () -> t.List[_Member]
        """
        Get list with all users.

        :return: list
        """
        members_res_lst = []  # type: t.List[_Member]
        members_url = self._service_data['context_memberships_url']  # type: t.Optional[str]

        while members_url:
            members, members_url = self.get_members_page(members_url)
            members_res_lst.extend(members)

        return members_res_lst

    def get_context(self):
        """
        Get context data.

        :return: dict
        """
        data = self.get_nrps_data()
        data_body = t.cast(t.Any, data.get('body', {}))
        return data_body.get('context', {})
