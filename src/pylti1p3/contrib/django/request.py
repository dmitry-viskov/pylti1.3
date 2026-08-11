from django.http import HttpRequest
from pylti1p3.request import Request


class DjangoRequest(Request):
    _post_only = False
    _default_params = None

    @property
    def session(self):
        return self.request.session

    def __init__(
        self,
        request: HttpRequest,
        post_only: bool = False,
        default_params=None,
    ):
        self.request = request
        self._post_only = post_only
        self._default_params = default_params if default_params else {}

    def get_param(self, key):
        if self._post_only:
            return self.request.POST.get(key, self._default_params.get(key))
        return self.request.GET.get(
            key, self.request.POST.get(key, self._default_params.get(key))
        )

    def get_cookie(self, key):
        return self.request.COOKIES.get(key)

    def is_secure(self):
        return self.request.is_secure()
