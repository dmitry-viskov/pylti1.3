import json


class LineItem(object):
    _id = None
    _score_maximum = None
    _label = None
    _resource_id = None
    _tag = None
    _start_date_time = None
    _end_date_time = None

    def __init__(self, lineitem=None):
        if not lineitem:
            lineitem = {}
        self._id = lineitem.get("id")
        self._score_maximum = lineitem.get("scoreMaximum")
        self._label = lineitem.get("label")
        self._resource_id = lineitem.get("resourceId")
        self._tag = lineitem.get("tag")
        self._start_date_time = lineitem.get("startDateTime")
        self._end_date_time = lineitem.get("endDateTime")

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value
        return self

    def get_label(self):
        return self._label

    def set_label(self, value):
        self._label = value
        return self

    def get_score_maximum(self):
        return self._score_maximum

    def set_score_maximum(self, value):
        self._score_maximum = value
        return self

    def get_resource_id(self):
        return self._resource_id

    def set_resource_id(self, value):
        self._resource_id = value
        return self

    def get_tag(self):
        return self._tag

    def set_tag(self, value):
        self._tag = value
        return self

    def get_start_date_time(self):
        return self._start_date_time

    def set_start_date_time(self, value):
        self._start_date_time = value
        return self

    def get_end_date_time(self):
        return self._end_date_time

    def set_end_date_time(self, value):
        self._end_date_time = value
        return self

    def get_value(self):
        data = {
            'id': self._id if self._id else None,
            'scoreMaximum': self._score_maximum if self._score_maximum else None,
            'label': self._label,
            'resourceId': self._resource_id,
            'tag': self._tag,
            'startDateTime': self._start_date_time,
            'endDateTime': self._end_date_time
        }
        return json.dumps({k: v for k, v in data.items() if v})
