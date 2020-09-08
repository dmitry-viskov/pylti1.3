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

    def put_grade(self, grade, line_item=None):
        # type: (Grade, t.Optional[LineItem]) -> _ServiceConnectorResponse
        if "https://purl.imsglobal.org/spec/lti-ags/scope/score" not in self._service_data['scope']:
            raise LtiException('Missing required scope')

        if line_item and not line_item.get_id():
            line_item = self.find_or_create_lineitem(line_item)
            score_url = line_item.get_id()
        elif not line_item and self._service_data.get('lineitem'):
            score_url = self._service_data.get('lineitem')
        else:
            if not line_item:
                line_item = LineItem()
                line_item.set_label('default')\
                    .set_score_maximum(100)
                line_item = self.find_or_create_lineitem(line_item)
            score_url = line_item.get_id()

        assert score_url is not None
        score_url = self._add_url_path_ending(score_url, 'scores')
        return self._service_connector.make_service_request(
            self._service_data['scope'],
            score_url,
            is_post=True,
            data=grade.get_value(),
            content_type='application/vnd.ims.lis.v1.score+json'
        )

    def get_lineitems(self):
        # type: () -> list
        if "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem" not in self._service_data['scope']:
            raise LtiException('Missing required scope')

        line_items = self._service_connector.make_service_request(
            self._service_data['scope'],
            self._service_data['lineitems'],
            accept='application/vnd.ims.lis.v2.lineitemcontainer+json'
        )
        if not isinstance(line_items['body'], list):
            raise LtiException('Unknown response type received for line items')
        return line_items['body']

    def find_lineitem_by_id(self, ln_id):
        # type: (t.Optional[str]) -> t.Optional[LineItem]
        line_items = self.get_lineitems()

        for line_item in line_items:
            line_item_id = line_item.get('id')
            if line_item_id == ln_id:
                return LineItem(line_item)
        return None

    def find_lineitem_by_tag(self, tag):
        # type: (t.Optional[str]) -> t.Optional[LineItem]
        line_items = self.get_lineitems()

        for line_item in line_items:
            line_item_tag = line_item.get('tag')
            if line_item_tag == tag:
                return LineItem(line_item)
        return None

    def find_or_create_lineitem(self, new_line_item, find_by='tag'):
        # type: (LineItem, Literal['tag', 'id']) -> LineItem
        if find_by == 'tag':
            tag = new_line_item.get_tag()
            line_item = self.find_lineitem_by_tag(tag)
        elif find_by == 'id':
            line_id = new_line_item.get_id()
            line_item = self.find_lineitem_by_id(line_id)
        else:
            raise LtiException('Invalid "find_by" value: ' + str(find_by))

        if line_item:
            return line_item

        created_line_item = self._service_connector.make_service_request(
            self._service_data['scope'],
            self._service_data['lineitems'],
            is_post=True,
            data=new_line_item.get_value(),
            content_type='application/vnd.ims.lis.v2.lineitem+json',
            accept='application/vnd.ims.lis.v2.lineitem+json'
        )
        if not isinstance(created_line_item['body'], dict):
            raise LtiException('Unknown response type received for create line item')
        return LineItem(created_line_item['body'])

    def get_grades(self, line_item):
        # type: (LineItem) -> list
        line_item_id = line_item.get_id()
        line_item_tag = line_item.get_tag()

        find_by = None  # type: t.Optional[Literal['id', 'tag']]
        if line_item_id:
            find_by = 'id'
        elif line_item_tag:
            find_by = 'tag'
        else:
            raise LtiException('Received LineItem did not contain a tag or id')

        line_item = self.find_or_create_lineitem(line_item, find_by=find_by)
        line_item_id = line_item.get_id()
        assert line_item_id is not None
        results_url = self._add_url_path_ending(line_item_id, 'results')
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
