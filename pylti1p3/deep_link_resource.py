import typing as t
from .lineitem import LineItem


class DeepLinkResource:
    _type: str = "ltiResourceLink"
    _title: t.Optional[str] = None
    _url: t.Optional[str] = None
    _lineitem: t.Optional[LineItem] = None
    _custom_params: t.Mapping[str, str] = {}
    _target: str = "iframe"
    _icon_url: t.Optional[str] = None

    def get_type(self):
        return self._type

    def set_type(self, value: str) -> "DeepLinkResource":
        self._type = value
        return self

    def get_title(self) -> t.Optional[str]:
        return self._title

    def set_title(self, value: str) -> "DeepLinkResource":
        self._title = value
        return self

    def get_url(self) -> t.Optional[str]:
        return self._url

    def set_url(self, value: str) -> "DeepLinkResource":
        self._url = value
        return self

    def get_lineitem(self) -> t.Optional[LineItem]:
        return self._lineitem

    def set_lineitem(self, value: LineItem) -> "DeepLinkResource":
        self._lineitem = value
        return self

    def get_custom_params(self) -> t.Mapping[str, str]:
        return self._custom_params

    def set_custom_params(self, value: t.Mapping[str, str]) -> "DeepLinkResource":
        self._custom_params = value
        return self

    def get_target(self) -> str:
        return self._target

    def set_target(self, value: str) -> "DeepLinkResource":
        self._target = value
        return self

    def get_icon_url(self) -> t.Optional[str]:
        return self._icon_url

    def set_icon_url(self, value: str) -> "DeepLinkResource":
        self._icon_url = value
        return self

    def to_dict(self) -> t.Dict[str, object]:
        res: t.Dict[str, object] = {
            "type": self._type,
            "title": self._title,
            "url": self._url,
            "custom": self._custom_params,
        }
        if self._lineitem:
            line_item: t.Dict[str, object] = {
                "scoreMaximum": self._lineitem.get_score_maximum(),
            }

            label = self._lineitem.get_label()
            if label:
                line_item["label"] = label

            resource_id = self._lineitem.get_resource_id()
            if resource_id:
                line_item["resourceId"] = resource_id

            tag = self._lineitem.get_tag()
            if tag:
                line_item["tag"] = tag

            submission_review = self._lineitem.get_submission_review()
            if submission_review:
                line_item["submissionReview"] = submission_review

            res["lineItem"] = line_item

        if self._icon_url:
            res["icon"] = {"url": self._icon_url}

        return res
