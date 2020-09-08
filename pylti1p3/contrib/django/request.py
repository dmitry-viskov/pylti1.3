from pylti1p3.request import Request


class DjangoRequest(Request):
    _request = None
    _post_only = False
    _default_params = None

    @property
    def session(self):
        return self._request.session

    def __init__(self, request, post_only=False, default_params=None):
        self.set_request(request)
        self._post_only = post_only
        self._default_params = default_params if default_params else {}

    def set_request(self, request):
        self._request = request

    def get_param(self, key):
        if self._post_only:
            return self._request.POST.get(key, self._default_params.get(key))
        return self._request.GET.get(key, self._request.POST.get(key, self._default_params.get(key)))

    def get_cookie(self, key):
        return self._request.COOKIES.get(key)

    def is_secure(self):
        return self._request.is_secure()
