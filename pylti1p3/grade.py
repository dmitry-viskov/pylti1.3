import json
import typing as t

if t.TYPE_CHECKING:
    T_SELF = t.TypeVar('T_SELF', bound='Grade')
    EXTRA_CLAIMS = t.Mapping[str, t.Any]


class Grade(object):
    _score_given = None  # type: t.Optional[float]
    _score_maximum = None  # type: t.Optional[float]
    _activity_progress = None  # type: t.Optional[str]
    _grading_progress = None  # type: t.Optional[str]
    _timestamp = None  # type: t.Optional[str]
    _user_id = None  # type: t.Optional[str]
    _extra_claims = None  # type: t.Optional[EXTRA_CLAIMS]

    def get_score_given(self):
        # type: () -> t.Optional[float]
        return self._score_given

    def set_score_given(self, value):
        # type: (T_SELF, float) -> T_SELF
        self._score_given = value
        return self

    def get_score_maximum(self):
        # type: () -> t.Optional[float]
        return self._score_maximum

    def set_score_maximum(self, value):
        # type: (T_SELF, float) -> T_SELF
        self._score_maximum = value
        return self

    def get_activity_progress(self):
        # type: () -> t.Optional[str]
        return self._activity_progress

    def set_activity_progress(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._activity_progress = value
        return self

    def get_grading_progress(self):
        # type: () -> t.Optional[str]
        return self._grading_progress

    def set_grading_progress(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._grading_progress = value
        return self

    def get_timestamp(self):
        # type: () -> t.Optional[str]
        return self._timestamp

    def set_timestamp(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._timestamp = value
        return self

    def get_user_id(self):
        # type: () -> t.Optional[str]
        return self._user_id

    def set_user_id(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._user_id = value
        return self

    def set_extra_claims(self, value):
        # type: (T_SELF, EXTRA_CLAIMS) -> T_SELF
        self._extra_claims = value
        return self

    def get_extra_claims(self):
        # type: () -> t.Optional[EXTRA_CLAIMS]
        return self._extra_claims

    def get_value(self):
        # type: () -> str
        data = {
            'scoreGiven': self._score_given if self._score_given else None,
            'scoreMaximum': self._score_maximum if self._score_maximum else None,
            'activityProgress': self._activity_progress,
            'gradingProgress': self._grading_progress,
            'timestamp': self._timestamp,
            'userId': self._user_id
        }
        if self._extra_claims is not None:
            data.update(self._extra_claims)

        return json.dumps({k: v for k, v in data.items() if v is not None})
