from .exception import LtiException
from .lineitem import LineItem


class AssignmentsGradesService(object):
    _service_connector = None
    _service_data = None

    def __init__(self, service_connector, service_data):
        self._service_connector = service_connector
        self._service_data = service_data

    def put_grade(self, grade, line_item=None):
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

        score_url += '/scores'
        return self._service_connector.make_service_request(
            self._service_data['scope'],
            score_url,
            is_post=True,
            data=grade.get_value(),
            content_type='application/vnd.ims.lis.v1.score+json'
        )

    def get_lineitems(self):
        if "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem" not in self._service_data['scope']:
            raise LtiException('Missing required scope')

        line_items = self._service_connector.make_service_request(
            self._service_data['scope'],
            self._service_data['lineitems'],
            accept='application/vnd.ims.lis.v2.lineitemcontainer+json'
        )
        return line_items['body']

    def find_lineitem_by_id(self, ln_id):
        line_items = self.get_lineitems()

        for line_item in line_items:
            line_item_id = line_item.get('id')
            if line_item_id == ln_id:
                return LineItem(line_item)
        return None

    def find_lineitem_by_tag(self, tag):
        line_items = self.get_lineitems()

        for line_item in line_items:
            line_item_tag = line_item.get('tag')
            if line_item_tag == tag:
                return LineItem(line_item)
        return None

    def find_or_create_lineitem(self, new_line_item, find_by='tag'):
        if find_by == 'tag':
            line_item = self.find_lineitem_by_tag(new_line_item.get_tag())
        elif find_by == 'id':
            line_item = self.find_lineitem_by_id(new_line_item.get_id())
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
        return LineItem(created_line_item['body'])

    def get_grades(self, line_item):
        line_item_id = line_item.get_id()
        line_item_tag = line_item.get_tag()

        find_by = None
        if line_item_id:
            find_by = 'id'
        elif line_item_tag:
            find_by = 'tag'

        line_item = self.find_or_create_lineitem(line_item, find_by=find_by)
        scores = self._service_connector.make_service_request(
            self._service_data['scope'],
            line_item.get_id() + '/results',
            accept='application/vnd.ims.lis.v2.resultcontainer+json'
        )
        return scores['body']
