import typing as t

from .utils import add_param_to_url


if t.TYPE_CHECKING:
    from .service_connector import ServiceConnector
    from mypy_extensions import TypedDict
    from typing_extensions import Literal

    _GroupsServiceData = TypedDict('_GroupsServiceData', {
        # Required data
        'context_groups_url': str,
        'scope': t.List[Literal['https://purl.imsglobal.org/spec/lti-gs/scope/contextgroup.readonly']],
        'service_versions': t.List[str],

        # Optional data
        'context_group_sets_url': str
    }, total=False)

    _Group = TypedDict('_Group', {
        # Required data
        'id': t.Union[str, int],
        'name': str,

        # Optional data
        'tag': str,
        'set_id': t.Union[str, int]
    }, total=False)

    _Set = TypedDict('_Set', {
        # Required data
        'id': t.Union[str, int],
        'name': str,

        # Optional data
        'groups': t.List[_Group]
    }, total=False)


class CourseGroupsService(object):
    _service_connector = None  # type: ServiceConnector
    _service_data = None  # type: _GroupsServiceData

    def __init__(self, service_connector, groups_service_data):
        # type: (ServiceConnector, _GroupsServiceData) -> None
        self._service_connector = service_connector
        self._service_data = groups_service_data

    def get_page(self, data_url, data_key='groups'):
        # type: (str, t.Optional[str]) -> t.Tuple[list, t.Optional[str]]
        """
        Get one page with the groups/sets.

        :param data_url
        :param data_key
        :return: tuple in format: (list with data items, next page url)
        """
        data = self._service_connector.make_service_request(
            self._service_data['scope'],
            data_url,
            accept='application/vnd.ims.lti-gs.v1.contextgroupcontainer+json',
        )
        data_body = t.cast(t.Any, data.get('body', {}))
        return data_body.get(data_key, []), data['next_page_url']

    def get_groups(self, user_id=None):
        groups_res_lst = []  # type: t.List[_Group]
        groups_url = self._service_data.get('context_groups_url')  # type: t.Optional[str]
        if user_id:
            groups_url = add_param_to_url(groups_url, 'user_id', user_id)

        while groups_url:
            groups, groups_url = self.get_page(groups_url, data_key='groups')
            groups_res_lst.extend(groups)

        return groups_res_lst

    def has_sets(self):
        return 'context_group_sets_url' in self._service_data

    def get_sets(self, include_groups=False):
        sets_res_lst = []  # type: t.List[_Set]
        sets_url = self._service_data.get('context_group_sets_url')  # type: t.Optional[str]

        while sets_url:
            sets, sets_url = self.get_page(sets_url, data_key='sets')
            sets_res_lst.extend(sets)

        if include_groups and sets_res_lst:
            set_id_to_index = {}
            for i, s in enumerate(sets_res_lst):
                set_id_to_index[s['id']] = i
                sets_res_lst[i]['groups'] = []

            groups = self.get_groups()
            for group in groups:
                set_id = group.get('set_id')
                if set_id and set_id in set_id_to_index:
                    index = set_id_to_index[set_id]
                    sets_res_lst[index]['groups'].append(group)

        return sets_res_lst
