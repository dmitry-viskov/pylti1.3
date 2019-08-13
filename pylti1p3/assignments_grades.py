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
        elif not line_item and not self._service_data.get('lineitem'):
            score_url = self._service_data.get('lineitem')
        else:
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

    def find_or_create_lineitem(self, new_line_item):
        if "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem" not in self._service_data['scope']:
            raise LtiException('Missing required scope')

        line_items = self._service_connector.make_service_request(
            self._service_data['scope'],
            self._service_data['lineitems'],
            accept='application/vnd.ims.lis.v2.lineitemcontainer+json'
        )

        for line_item in line_items['body']:
            if line_item['tag'] == new_line_item.get_tag():
                return LineItem(line_item)

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
        line_item = self.find_or_create_lineitem(line_item)
        scores = self._service_connector.make_service_request(
            self._service_data['scope'],
            line_item.get_id() + '/results',
            accept='application/vnd.ims.lis.v2.resultcontainer+json'
        )
        return scores['body']
