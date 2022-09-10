import typing as t

from .exception import LtiException
from .lineitem import LineItem

if t.TYPE_CHECKING:
    from .service_connector import ServiceConnector, _ServiceConnectorResponse
    from .grade import Grade
    from mypy_extensions import TypedDict
    from typing_extensions import Literal

    _AssignmentsGradersData = TypedDict('_AssignmentsGradersData', {
        'scope': t.List[Literal['https://purl.imsglobal.org/spec/lti-ags/scope/score',
                                'https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly',
                                'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem',
                                'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly']],
        'lineitems': str,
        'lineitem': str,
    }, total=False)


class AssignmentsGradesService(object):
    _service_connector = None  # type: ServiceConnector
    _service_data = None  # type: _AssignmentsGradersData

    def __init__(self, service_connector, service_data):
        # type: (ServiceConnector, _AssignmentsGradersData) -> None
        self._service_connector = service_connector
        self._service_data = service_data

    def can_read_lineitem(self):
        return "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly" in self._service_data['scope']

    def can_create_lineitem(self):
        return "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem" in self._service_data['scope']

    def can_read_grades(self):
        return 'https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly' in self._service_data['scope']

    def can_put_grade(self):
        return "https://purl.imsglobal.org/spec/lti-ags/scope/score" in self._service_data['scope']

    def put_grade(self, grade, lineitem=None):
        # type: (Grade, t.Optional[LineItem]) -> _ServiceConnectorResponse
        """
        Send grade to the LTI platform.

        :param grade: Grade instance
        :param lineitem: LineItem instance
        :param create_default_lineitem: create default lineitem if nothing was found
        :param default_lineitem_tag: str
        :return: dict with HTTP response body and headers
        """

        if not self.can_put_grade():
            raise LtiException("Can't put grade: Missing required scope")

        if lineitem and not lineitem.get_id():
            lineitem = self.find_or_create_lineitem(lineitem)
            score_url = lineitem.get_id()
        elif not lineitem and self._service_data.get('lineitem'):
            score_url = self._service_data.get('lineitem')
        else:
            raise LtiException("Can't find lineitem to put grade")

        assert score_url is not None
        score_url = self._add_url_path_ending(score_url, 'scores')
        return self._service_connector.make_service_request(
            self._service_data['scope'],
            score_url,
            is_post=True,
            data=grade.get_value(),
            content_type='application/vnd.ims.lis.v1.score+json'
        )

    def get_lineitem(self, lineitem_url=None):
        """
        Retrieves an individual lineitem. By default retrieves the lineitem
        associated with the LTI message.

        :param lineitem_url: endpoint for LTI line item (optional)
        :return: LineItem instance
        """
        if not self.can_read_lineitem():
            raise LtiException("Can't read lineitem: Missing required scope")

        if lineitem_url is None:
            lineitem_url = self._service_data['lineitem']

        lineitem_response = self._service_connector.make_service_request(
            self._service_data['scope'],
            lineitem_url,
            accept='application/vnd.ims.lis.v2.lineitem+json',
        )
        return LineItem(lineitem_response['body'])

    def get_lineitems_page(self, lineitems_url=None):
        # type: (t.Optional[str]) -> t.Tuple[list, t.Optional[str]]
        """
        Get one page with line items.

        :param lineitems_url: LTI platform's URL (optional)
        :return: tuple in format: (list with line items, next page url)
        """
        if not self.can_read_lineitem():
            raise LtiException("Can't read lineitem: Missing required scope")

        if not lineitems_url:
            lineitems_url = self._service_data['lineitems']

        lineitems = self._service_connector.make_service_request(
            self._service_data['scope'],
            lineitems_url,
            accept='application/vnd.ims.lis.v2.lineitemcontainer+json'
        )
        if not isinstance(lineitems['body'], list):
            raise LtiException('Unknown response type received for line items')
        return lineitems['body'], lineitems['next_page_url']

    def get_lineitems(self):
        # type: () -> list
        """
        Get list of all available line items.

        :return: list
        """
        lineitems_res_lst = []
        lineitems_url = self._service_data['lineitems']  # type: t.Optional[str]

        while lineitems_url:
            lineitems, lineitems_url = self.get_lineitems_page(lineitems_url)
            lineitems_res_lst.extend(lineitems)

        return lineitems_res_lst

    def find_lineitem(self, prop_name, prop_value):
        # type: (str, t.Any) -> t.Optional[LineItem]
        """
        Find line item by some property (ID/Tag).

        :param prop_name: property name
        :param prop_value: property value
        :return: LineItem instance or None
        """
        lineitems_url = self._service_data['lineitems']  # type: t.Optional[str]

        while lineitems_url:
            lineitems, lineitems_url = self.get_lineitems_page(lineitems_url)
            for lineitem in lineitems:
                lineitem_prop_value = lineitem.get(prop_name)
                if lineitem_prop_value == prop_value:
                    return LineItem(lineitem)
        return None

    def find_lineitem_by_id(self, ln_id):
        # type: (str) -> t.Optional[LineItem]
        """
        Find line item by ID.

        :param ln_id: str
        :return: LineItem instance or None
        """
        return self.find_lineitem('id', ln_id)

    def find_lineitem_by_tag(self, tag):
        # type: (str) -> t.Optional[LineItem]
        """
        Find line item by Tag.

        :param tag: str
        :return: LineItem instance or None
        """
        return self.find_lineitem('tag', tag)

    def find_lineitem_by_resource_link_id(self, resource_link_id):
        # type: (str) -> t.Optional[LineItem]
        """
        Find line item by Resource LinkID.

        :param resource_link_id: str
        :return: LineItem instance or None
        """
        return self.find_lineitem('resourceLinkId', resource_link_id)

    def find_lineitem_by_resource_id(self, resource_id):
        # type: (str) -> t.Optional[LineItem]
        """
        Find line item by Resource ID.

        :param resource_id: str
        :return: LineItem instance or None
        """
        return self.find_lineitem('resourceId', resource_id)

    def find_or_create_lineitem(self, new_lineitem, find_by='tag'):
        # type: (LineItem, Literal['tag', 'resource_link_id', 'resource_id', 'id']) -> LineItem
        """
        Try to find line item using ID or Tag. New lime item will be created if nothing is found.

        :param new_lineitem: LineItem instance
        :param find_by: str ("tag"/"id")
        :return: LineItem instance (based on response from the LTI platform)
        """
        if find_by == 'tag':
            tag = new_lineitem.get_tag()
            if not tag:
                raise LtiException('Tag value is not specified')
            lineitem = self.find_lineitem_by_tag(tag)
        elif find_by == 'id':
            line_id = new_lineitem.get_id()
            if not line_id:
                raise LtiException('ID value is not specified')
            lineitem = self.find_lineitem_by_id(line_id)
        elif find_by == 'resource_link_id':
            resource_link_id = new_lineitem.get_resource_link_id()
            if not resource_link_id:
                raise LtiException('Resource Link ID value is not specified')
            lineitem = self.find_lineitem_by_resource_link_id(resource_link_id)
        elif find_by == 'resource_id':
            resource_id = new_lineitem.get_resource_id()
            if not resource_id:
                raise LtiException('Resource ID value is not specified')
            lineitem = self.find_lineitem_by_resource_id(resource_id)
        else:
            raise LtiException('Invalid "find_by" value: ' + str(find_by))

        if lineitem:
            return lineitem

        if not self.can_create_lineitem():
            raise LtiException("Can't create lineitem: Missing required scope")

        created_lineitem = self._service_connector.make_service_request(
            self._service_data['scope'],
            self._service_data['lineitems'],
            is_post=True,
            data=new_lineitem.get_value(),
            content_type='application/vnd.ims.lis.v2.lineitem+json',
            accept='application/vnd.ims.lis.v2.lineitem+json'
        )
        if not isinstance(created_lineitem['body'], dict):
            raise LtiException('Unknown response type received for create line item')
        return LineItem(created_lineitem['body'])

    def get_grades(self, lineitem=None):
        # type: (t.Optional[LineItem]) -> list
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
            lineitem_id = self._service_data.get('lineitem')

        if not lineitem_id:
            return []

        results_url = self._add_url_path_ending(lineitem_id, 'results')
        scores = self._service_connector.make_service_request(
            self._service_data['scope'],
            results_url,
            accept='application/vnd.ims.lis.v2.resultcontainer+json'
        )
        if not isinstance(scores['body'], list):
            raise LtiException('Unknown response type received for results')
        return scores['body']

    def _add_url_path_ending(self, url, url_path_ending):
        # type: (str, str) -> str
        if '?' in url:
            url_parts = url.split('?')
            new_url = url_parts[0]
            new_url += '' if new_url.endswith('/') else '/'
            return new_url + url_path_ending + '?' + url_parts[1]
        else:
            url += '' if url.endswith('/') else '/'
            return url + url_path_ending
