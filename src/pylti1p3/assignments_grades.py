from collections.abc import Generator, Callable
import typing as t
import typing_extensions as te
from .exception import LtiException
from .lineitem import LineItem
from .grade import Grade
from .lineitem import TLineItem
from .service_connector import ServiceConnector, TServiceConnectorResponse


TAssignmentsGradersData = te.TypedDict(
    "TAssignmentsGradersData",
    {
        "scope": t.List[
            te.Literal[
                "https://purl.imsglobal.org/spec/lti-ags/scope/score",
                "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly",
                "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
                "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly",
            ]
        ],
        "lineitems": str,
        "lineitem": str,
    },
    total=False,
)


class AssignmentsGradesService:
    _service_connector: ServiceConnector
    _service_data: TAssignmentsGradersData

    def __init__(
        self, service_connector: ServiceConnector, service_data: TAssignmentsGradersData
    ):
        self._service_connector = service_connector
        self._service_data = service_data

    def can_read_lineitem(self) -> bool:
        return (
            "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly"
            in self._service_data["scope"]
            or "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"
            in self._service_data["scope"]
        )

    def can_create_lineitem(self) -> bool:
        return (
            "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"
            in self._service_data["scope"]
        )

    def can_read_grades(self) -> bool:
        return (
            "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly"
            in self._service_data["scope"]
        )

    def can_put_grade(self) -> bool:
        return (
            "https://purl.imsglobal.org/spec/lti-ags/scope/score"
            in self._service_data["scope"]
        )

    def put_grade(
        self, grade: Grade, lineitem: t.Optional[LineItem] = None
    ) -> TServiceConnectorResponse:
        """
        Send grade to the LTI platform.

        :param grade: Grade instance
        :param lineitem: LineItem instance
        :return: dict with HTTP response body and headers
        """

        if not self.can_put_grade():
            raise LtiException("Can't put grade: Missing required scope")

        if lineitem:
            if not lineitem.get_id():
                lineitem = self.find_or_create_lineitem(lineitem)
            score_url = lineitem.get_id()
        elif not lineitem and self._service_data.get("lineitem"):
            score_url = self._service_data.get("lineitem")
        else:
            raise LtiException("Can't find lineitem to put grade")

        assert score_url is not None
        score_url = self._add_url_path_ending(score_url, "scores")
        return self._service_connector.make_service_request(
            self._service_data["scope"],
            score_url,
            is_post=True,
            data=grade.get_value(),
            content_type="application/vnd.ims.lis.v1.score+json",
        )

    def get_lineitem(self, lineitem_url: t.Optional[str] = None):
        """
        Retrieves an individual lineitem. By default retrieves the lineitem
        associated with the LTI message.

        :param lineitem_url: endpoint for LTI line item (optional)
        :return: LineItem instance
        """
        if not self.can_read_lineitem():
            raise LtiException("Can't read lineitem: Missing required scope")

        if lineitem_url is None:
            lineitem_url = self._service_data["lineitem"]

        lineitem_response = self._service_connector.make_service_request(
            self._service_data["scope"],
            lineitem_url,
            accept="application/vnd.ims.lis.v2.lineitem+json",
        )
        return LineItem(t.cast(TLineItem, lineitem_response["body"]))

    def get_lineitems_page(
        self, lineitems_url: t.Optional[str] = None
    ) -> t.Tuple[list, t.Optional[str]]:
        """
        Get one page with line items.

        :param lineitems_url: LTI platform's URL (optional)
        :return: tuple in format: (list with line items, next page url)
        """
        if not self.can_read_lineitem():
            raise LtiException("Can't read lineitem: Missing required scope")

        if not lineitems_url:
            lineitems_url = self._service_data["lineitems"]

        lineitems = self._service_connector.make_service_request(
            self._service_data["scope"],
            lineitems_url,
            accept="application/vnd.ims.lis.v2.lineitemcontainer+json",
        )
        if not isinstance(lineitems["body"], list):
            raise LtiException("Unknown response type received for line items")
        return lineitems["body"], lineitems["next_page_url"]

    def get_lineitems(self) -> Generator[TLineItem]:
        """
        Get list of all available line items.

        :return: list
        """
        lineitems_url: t.Optional[str] = self._service_data["lineitems"]

        if lineitems_url is None:
            return

        lineitem_pages = self._service_connector.get_paginated_data(
            self._service_data["scope"],
            lineitems_url,
            accept="application/vnd.ims.lis.v2.lineitemcontainer+json",
        )

        for page in lineitem_pages:
            if not isinstance(page["body"], list):
                raise LtiException("Unknown response type received for line items")

            yield from [t.cast(TLineItem, item) for item in page["body"]]

    def find_lineitem_satisfying(
        self, condition: Callable[[TLineItem], bool]
    ) -> t.Optional[LineItem]:
        """
        Find line item matching the given condition.

        :param condition: A function which takes a line item's dict representation and returns a bool.
        :return: LineItem instance or None
        """
        for lineitem_dict in self.get_lineitems():
            if condition(lineitem_dict):
                return LineItem(lineitem_dict)
        return None

    def find_lineitem(self, prop_name: str, prop_value: t.Any) -> t.Optional[LineItem]:
        """
        Find line item by some property (ID/Tag).

        :param prop_name: property name
        :param prop_value: property value
        :return: LineItem instance or None
        """
        return self.find_lineitem_satisfying(lambda x: x.get(prop_name) == prop_value)

    def find_lineitem_by_id(self, ln_id: str) -> t.Optional[LineItem]:
        """
        Find line item by ID.

        :param ln_id: str
        :return: LineItem instance or None
        """
        return self.find_lineitem("id", ln_id)

    def find_lineitem_by_tag(self, tag: str) -> t.Optional[LineItem]:
        """
        Find line item by Tag.

        :param tag: str
        :return: LineItem instance or None
        """
        return self.find_lineitem("tag", tag)

    def find_lineitem_by_resource_link_id(
        self, resource_link_id: str
    ) -> t.Optional[LineItem]:
        """
        Find line item by Resource LinkID.

        :param resource_link_id: str
        :return: LineItem instance or None
        """
        return self.find_lineitem("resourceLinkId", resource_link_id)

    def find_lineitem_by_resource_id(self, resource_id: str) -> t.Optional[LineItem]:
        """
        Find line item by Resource ID.

        :param resource_id: str
        :return: LineItem instance or None
        """
        return self.find_lineitem("resourceId", resource_id)

    def find_or_create_lineitem(
        self,
        new_lineitem: LineItem,
        find_by: str = "tag",
        condition: t.Optional[Callable[[TLineItem], bool]] = None,
    ) -> LineItem:
        """
        Try to find line item using ID or Tag. New lime item will be created if nothing is found.

        :param new_lineitem: LineItem instance
        :param find_by: str ("tag"/"id")
        :return: LineItem instance (based on response from the LTI platform)
        """
        if condition is not None:
            lineitem = self.find_lineitem_satisfying(condition)
        elif find_by == "tag":
            tag = new_lineitem.get_tag()
            if not tag:
                raise LtiException("Tag value is not specified")
            lineitem = self.find_lineitem_by_tag(tag)
        elif find_by == "id":
            line_id = new_lineitem.get_id()
            if not line_id:
                raise LtiException("ID value is not specified")
            lineitem = self.find_lineitem_by_id(line_id)
        elif find_by == "resource_link_id":
            resource_link_id = new_lineitem.get_resource_link_id()
            if not resource_link_id:
                raise LtiException("Resource Link ID value is not specified")
            lineitem = self.find_lineitem_by_resource_link_id(resource_link_id)
        elif find_by == "resource_id":
            resource_id = new_lineitem.get_resource_id()
            if not resource_id:
                raise LtiException("Resource ID value is not specified")
            lineitem = self.find_lineitem_by_resource_id(resource_id)
        else:
            raise LtiException('Invalid "find_by" value: ' + str(find_by))

        if lineitem:
            return lineitem

        created_lineitem = self.create_lineitem(new_lineitem)

        return created_lineitem

    def create_lineitem(self, new_lineitem: LineItem) -> LineItem:
        """
        Create a line item on the platform.
        """
        if not self.can_create_lineitem():
            raise LtiException("Can't create lineitem: Missing required scope")

        response = self._service_connector.make_service_request(
            scopes=self._service_data["scope"],
            url=self._service_data["lineitems"],
            is_post=True,
            data=new_lineitem.get_value(),
            content_type="application/vnd.ims.lis.v2.lineitem+json",
            accept="application/vnd.ims.lis.v2.lineitem+json",
        )
        if not isinstance(response["body"], dict):
            raise LtiException("Unknown response type received for create line item")

        return LineItem(t.cast(TLineItem, response["body"]))

    def get_grades(self, lineitem: t.Optional[LineItem] = None) -> Generator:
        """
        Return all grades for the passed line item (across all users enrolled in the line item's context).

        :param lineitem: LineItem instance
        :return: list of grades
        """
        if not self.can_read_grades():
            raise LtiException("Can't read grades: Missing required scope")

        if lineitem:
            lineitem_id = lineitem.get_id()
        else:
            lineitem_id = self._service_data.get("lineitem")

        if not lineitem_id:
            return

        results_url = self._add_url_path_ending(lineitem_id, "results")
        score_pages = self._service_connector.get_paginated_data(
            self._service_data["scope"],
            results_url,
            accept="application/vnd.ims.lis.v2.resultcontainer+json",
        )
        for page in score_pages:
            if not isinstance(page["body"], list):
                raise LtiException("Unknown response type received for results")

            yield from page["body"]

    @staticmethod
    def _add_url_path_ending(url: str, url_path_ending: str) -> str:
        if "?" in url:
            url_parts = url.split("?")
            new_url = url_parts[0]
            new_url += "" if new_url.endswith("/") else "/"
            return new_url + url_path_ending + "?" + url_parts[1]
        url += "" if url.endswith("/") else "/"
        return url + url_path_ending
