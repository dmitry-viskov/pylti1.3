from datetime import datetime
import json
import typing as t
from .exception import LtiException


TExtraClaims = t.Mapping[str, t.Any]


def remove_nones(value: dict) -> dict:
    return {
        k: remove_nones(v) if isinstance(v, dict) else v
        for k, v in value.items()
        if v is not None
    }


def format_time(time: t.Union[str, datetime]) -> str:
    if isinstance(time, datetime):
        return time.strftime("%Y-%m-%dT%H:%M:%S%z")

    return time


class Grade:
    _score_given: t.Optional[float] = None
    _score_maximum: t.Optional[float] = None
    _activity_progress: t.Optional[str] = None
    _grading_progress: t.Optional[str] = None
    _timestamp: t.Optional[str] = None
    _started_at: t.Optional[str] = None
    _submitted_at: t.Optional[str] = None
    _user_id: t.Optional[str] = None
    _comment: t.Optional[str] = None
    _extra_claims: t.Optional[TExtraClaims] = None

    def _validate_score(self, score_value) -> t.Optional[str]:
        if not isinstance(score_value, (int, float)):
            return "score must be integer or float"
        if score_value < 0:
            return "score must be positive number (including 0)"
        return None

    def get_score_given(self) -> t.Optional[float]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoregiven-and-scoremaximum
        """
        return self._score_given

    def set_score_given(self, value: float) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoregiven-and-scoremaximum
        """
        err_msg = self._validate_score(value)
        if err_msg is not None:
            raise LtiException("Invalid scoreGiven value: " + err_msg)
        self._score_given = value
        return self

    def get_score_maximum(self) -> t.Optional[float]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoregiven-and-scoremaximum
        """
        return self._score_maximum

    def set_score_maximum(self, value: float) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#scoregiven-and-scoremaximum
        """
        err_msg = self._validate_score(value)
        if err_msg is not None:
            raise LtiException("Invalid scoreMaximum value: " + err_msg)
        self._score_maximum = value
        return self

    def get_activity_progress(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#activityprogress
        """
        return self._activity_progress

    def set_activity_progress(self, value: str) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#activityprogress
        """
        self._activity_progress = value
        return self

    def get_grading_progress(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#gradingprogress
        """
        return self._grading_progress

    def set_grading_progress(self, value: str) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#gradingprogress
        """
        self._grading_progress = value
        return self

    def get_timestamp(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#timestamp
        """
        return self._timestamp

    def set_timestamp(self, value: t.Union[str, datetime]) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#timestamp
        """
        self._timestamp = format_time(value)
        return self

    def get_started_at(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#startedat-optional
        """
        return self._started_at

    def set_started_at(self, value: t.Union[str, datetime]) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#startedat-optional
        """
        self._started_at = format_time(value)
        return self

    def get_submitted_at(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#submittedat-optional
        """
        return self._submitted_at

    def set_submitted_at(self, value: t.Union[str, datetime]) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#submittedat-optional
        """
        self._submitted_at = format_time(value)
        return self

    def get_user_id(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#userid-0
        """
        return self._user_id

    def set_user_id(self, value: str) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#userid-0
        """
        self._user_id = value
        return self

    def get_comment(self) -> t.Optional[str]:
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#comment-0
        """
        return self._comment

    def set_comment(self, value: str) -> "Grade":
        """
        https://www.imsglobal.org/spec/lti-ags/v2p0/#comment-0
        """
        self._comment = value
        return self

    def set_extra_claims(self, value: TExtraClaims) -> "Grade":
        self._extra_claims = value
        return self

    def get_extra_claims(self) -> t.Optional[TExtraClaims]:
        return self._extra_claims

    def get_value(self) -> str:
        data: dict[str, t.Union[str, float, dict[str, t.Union[str, None]], None]]
        data = {
            "scoreGiven": self._score_given,
            "scoreMaximum": self._score_maximum,
            "activityProgress": self._activity_progress,
            "gradingProgress": self._grading_progress,
            "timestamp": self._timestamp,
            "userId": self._user_id,
            "comment": self._comment,
        }
        if self._started_at is not None or self._submitted_at is not None:
            data["submission"] = {
                "startedAt": self._started_at,
                "submittedAt": self._submitted_at,
            }
        if self._extra_claims is not None:
            data.update(self._extra_claims)

        return json.dumps(remove_nones(data))
