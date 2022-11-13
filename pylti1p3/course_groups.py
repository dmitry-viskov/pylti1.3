import typing as t
import typing_extensions as te
from .utils import add_param_to_url
from .service_connector import ServiceConnector

TGroupsServiceData = te.TypedDict(
    "TGroupsServiceData",
    {
        # Required data
        "context_groups_url": str,
        "scope": t.List[
            te.Literal[
                "https://purl.imsglobal.org/spec/lti-gs/scope/contextgroup.readonly"
            ]
        ],
        "service_versions": t.List[str],
        # Optional data
        "context_group_sets_url": str,
    },
    total=False,
)

TGroup = te.TypedDict(
    "TGroup",
    {
        # Required data
        "id": t.Union[str, int],
        "name": str,
        # Optional data
        "tag": str,
        "set_id": t.Union[str, int],
    },
    total=False,
)

TSet = te.TypedDict(
    "TSet",
    {
        # Required data
        "id": t.Union[str, int],
        "name": str,
        # Optional data
        "groups": t.List[TGroup],
    },
    total=False,
)


class CourseGroupsService:
    _service_connector: ServiceConnector
    _service_data: TGroupsServiceData

    def __init__(
        self,
        service_connector: ServiceConnector,
        groups_service_data: TGroupsServiceData,
    ):
        self._service_connector = service_connector
        self._service_data = groups_service_data

    def get_page(
        self, data_url: str, data_key: str = "groups"
    ) -> t.Tuple[list, t.Optional[str]]:
        """
        Get one page with the groups/sets.

        :param data_url
        :param data_key
        :return: tuple in format: (list with data items, next page url)
        """
        data = self._service_connector.make_service_request(
            self._service_data["scope"],
            data_url,
            accept="application/vnd.ims.lti-gs.v1.contextgroupcontainer+json",
        )
        data_body = t.cast(t.Any, data.get("body", {}))
        return data_body.get(data_key, []), data["next_page_url"]

    def get_groups(self, user_id=None):
        groups_res_lst = []
        groups_url = self._service_data.get("context_groups_url")
        if user_id:
            groups_url = add_param_to_url(groups_url, "user_id", user_id)

        while groups_url:
            groups, groups_url = self.get_page(groups_url, data_key="groups")
            groups_res_lst.extend(groups)

        return groups_res_lst

    def has_sets(self):
        return "context_group_sets_url" in self._service_data

    def get_sets(self, include_groups=False):
        sets_res_lst = []
        sets_url = self._service_data.get("context_group_sets_url")

        while sets_url:
            sets, sets_url = self.get_page(sets_url, data_key="sets")
            sets_res_lst.extend(sets)

        if include_groups and sets_res_lst:
            set_id_to_index = {}
            for i, s in enumerate(sets_res_lst):
                set_id_to_index[s["id"]] = i
                sets_res_lst[i]["groups"] = []

            groups = self.get_groups()
            for group in groups:
                set_id = group.get("set_id")
                if set_id and set_id in set_id_to_index:
                    index = set_id_to_index[set_id]
                    sets_res_lst[index]["groups"].append(group)

        return sets_res_lst
