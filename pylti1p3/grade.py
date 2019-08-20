import json


class Grade(object):
    _score_given = None
    _score_maximum = None
    _activity_progress = None
    _grading_progress = None
    _timestamp = None
    _user_id = None

    def get_score_given(self):
        return self._score_given

    def set_score_given(self, value):
        self._score_given = value
        return self

    def get_score_maximum(self):
        return self._score_maximum

    def set_score_maximum(self, value):
        self._score_maximum = value
        return self

    def get_activity_progress(self):
        return self._activity_progress

    def set_activity_progress(self, value):
        self._activity_progress = value
        return self

    def get_grading_progress(self):
        return self._grading_progress

    def set_grading_progress(self, value):
        self._grading_progress = value
        return self

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, value):
        self._timestamp = value
        return self

    def get_user_id(self):
        return self._user_id

    def set_user_id(self, value):
        self._user_id = value

    def get_value(self):
        data = {
            'scoreGiven': self._score_given if self._score_given else None,
            'scoreMaximum': self._score_maximum if self._score_maximum else None,
            'activityProgress': self._activity_progress,
            'gradingProgress': self._grading_progress,
            'timestamp': self._timestamp,
            'userId': self._user_id
        }
        return json.dumps({k: v for k, v in data.items() if v})
