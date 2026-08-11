import typing as t
import typing_extensions as te
from .utils import add_param_to_url
from .service_connector import ServiceConnector

TNamesAndRolesData = te.TypedDict(
    "TNamesAndRolesData",
    {
        "context_memberships_url": str,
    },
    total=False,
)

TMember = te.TypedDict(
    "TMember",
    {
        "name": str,
        "status": te.Literal["Active", "Inactive", "Deleted"],
        "picture": str,
        "given_name": str,
        "family_name": str,
        "middle_name": str,
        "email": str,
        "user_id": str,
        "lis_person_sourcedid": str,
        "roles": t.List[str],
        "message": t.Union[t.List[t.Dict[str, object]], t.Dict[str, object]],
        "lti11_legacy_user_id": t.Optional[str],
    },
    total=False,
)


class NamesRolesProvisioningService:
    _service_connector: ServiceConnector
    _service_data: TNamesAndRolesData

    def __init__(
        self, service_connector: ServiceConnector, service_data: TNamesAndRolesData
    ):
        self._service_connector = service_connector
        self._service_data = service_data

    def get_nrps_data(self, members_url: t.Optional[str] = None):
        if not members_url:
            members_url = self._service_data["context_memberships_url"]

        data = self._service_connector.make_service_request(
            [
                "https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly"
            ],
            members_url,
            accept="application/vnd.ims.lti-nrps.v2.membershipcontainer+json",
        )
        return data

    def get_members_page(
        self, members_url: t.Optional[str] = None
    ) -> t.Tuple[t.List[TMember], t.Optional[str]]:
        """
        Get one page with the users.

        :param members_url: LTI platform's URL (optional)
        :return: tuple in format: (list with users, next page url)
        """
        data = self.get_nrps_data(members_url=members_url)
        data_body = t.cast(t.Any, data.get("body", {}))
        return data_body.get("members", []), data["next_page_url"]

    def get_members(self, resource_link_id: t.Optional[str] = None) -> t.List[TMember]:
        """
        Get list with all users.

        :param resource_link_id: resource link id (optional)
        :return: list
        """
        members_res_lst: t.List[TMember] = []
        members_url: t.Optional[str] = self._service_data["context_memberships_url"]

        if members_url and resource_link_id:
            members_url = add_param_to_url(members_url, "rlid", resource_link_id)

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
        data_body = t.cast(t.Any, data.get("body", {}))
        return data_body.get("context", {})
