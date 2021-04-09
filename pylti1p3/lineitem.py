import json
import typing as t
from .exception import LtiException

if t.TYPE_CHECKING:
    T_SELF = t.TypeVar('T_SELF', bound='LineItem')


class LineItem(object):
    _id = None  # type: t.Optional[str]
    _score_maximum = None  # type: t.Optional[float]
    _label = None  # type: t.Optional[str]
    _resource_id = None  # type: t.Optional[str]
    _tag = None  # type: t.Optional[str]
    _start_date_time = None  # type: t.Optional[str]
    _end_date_time = None  # type: t.Optional[str]

    def __init__(self, lineitem=None):
        # type: (t.Optional[t.Mapping[str, t.Any]]) -> None
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
        # type: () -> t.Optional[str]
        return self._id

    def set_id(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._id = value
        return self

    def get_label(self):
        # type: () -> t.Optional[str]
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#label
        """
        return self._label

    def set_label(self, value):
        # type: (T_SELF, str) -> T_SELF
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#label
        """
        self._label = value
        return self

    def get_score_maximum(self):
        # type: () -> t.Optional[float]
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoremaximum
        """
        return self._score_maximum

    def set_score_maximum(self, value):
        # type: (T_SELF, float) -> T_SELF
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoremaximum
        """
        if not isinstance(value, (int, float)):
            raise LtiException('Invalid scoreMaximum value: score must be integer or float')
        if value <= 0:
            raise LtiException('Invalid scoreMaximum value: score must be non null value, strictly greater than 0')

        self._score_maximum = value
        return self

    def get_resource_id(self):
        # type: () -> t.Optional[str]
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tool-resource-identifier-resourceid
        """
        return self._resource_id

    def set_resource_id(self, value):
        # type: (T_SELF, str) -> T_SELF
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tool-resource-identifier-resourceid
        """
        self._resource_id = value
        return self

    def get_tag(self):
        # type: () -> t.Optional[str]
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tag
        """
        return self._tag

    def set_tag(self, value):
        # type: (T_SELF, str) -> T_SELF
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#tag
        """
        self._tag = value
        return self

    def get_start_date_time(self):
        # type: () -> t.Optional[str]
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#startdatetime
        """
        return self._start_date_time

    def set_start_date_time(self, value):
        # type: (T_SELF, str) -> T_SELF
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#startdatetime
        """
        self._start_date_time = value
        return self

    def get_end_date_time(self):
        # type: () -> t.Optional[str]
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#enddatetime
        """
        return self._end_date_time

    def set_end_date_time(self, value):
        # type: (T_SELF, str) -> T_SELF
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#enddatetime
        """
        self._end_date_time = value
        return self

    def get_value(self):
        # type: () -> str
        data = {
            'id': self._id if self._id else None,
            'scoreMaximum': self._score_maximum,
            'label': self._label,
            'resourceId': self._resource_id,
            'tag': self._tag,
            'startDateTime': self._start_date_time,
            'endDateTime': self._end_date_time
        }
        return json.dumps({k: v for k, v in data.items() if v})
