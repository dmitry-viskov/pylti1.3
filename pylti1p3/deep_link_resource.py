import typing as t

if t.TYPE_CHECKING:
    from .lineitem import LineItem
    T_SELF = t.TypeVar('T_SELF', bound='DeepLinkResource')


class DeepLinkResource(object):
    _type = 'ltiResourceLink'  # type: str
    _title = None  # type: t.Optional[str]
    _url = None  # type: t.Optional[str]
    _lineitem = None  # type: t.Optional[LineItem]
    _custom_params = {}  # type: t.Mapping[str, str]
    _target = 'iframe'  # type: str

    def get_type(self):
        # type: () -> str
        return self._type

    def set_type(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._type = value
        return self

    def get_title(self):
        # type: () -> t.Optional[str]
        return self._title

    def set_title(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._title = value
        return self

    def get_url(self):
        # type: () -> t.Optional[str]
        return self._url

    def set_url(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._url = value
        return self

    def get_lineitem(self):
        # type: () -> t.Optional[LineItem]
        return self._lineitem

    def set_lineitem(self, value):
        # type: (T_SELF, LineItem) -> T_SELF
        self._lineitem = value
        return self

    def get_custom_params(self):
        # type: () -> t.Mapping[str, str]
        return self._custom_params

    def set_custom_params(self, value):
        # type: (T_SELF, t.Mapping[str, str]) -> T_SELF
        self._custom_params = value
        return self

    def get_target(self):
        # type: () -> str
        return self._target

    def set_target(self, value):
        # type: (T_SELF, str) -> T_SELF
        self._target = value
        return self

    def to_dict(self):
        # type: () -> t.Dict[str, object]
        res = {
            'type': self._type,
            'title': self._title,
            'url': self._url,
            'custom': self._custom_params
        }  # type: t.Dict[str, object]
        if self._lineitem:
            line_item = {
                'scoreMaximum': self._lineitem.get_score_maximum(),
            }  # type: t.Dict[str, object]

            label = self._lineitem.get_label()
            if label:
                line_item['label'] = label

            resource_id = self._lineitem.get_resource_id()
            if resource_id:
                line_item['resourceId'] = resource_id

            tag = self._lineitem.get_tag()
            if tag:
                line_item['tag'] = tag

            submission_review = self._lineitem.get_submission_review()
            if submission_review:
                line_item['submissionReview'] = submission_review

            res['lineItem'] = line_item
        return res
