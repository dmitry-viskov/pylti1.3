from pylti1p3.request import Request


class DjangoRequest(Request):
    _request = None
    _post_only = False

    def __init__(self, request, post_only=False):
        self.set_request(request)
        self._post_only = post_only

    def set_request(self, request):
        self._request = request

    def get_param(self, key):
        if self._post_only:
            return self._request.POST.get(key, None)
        return self._request.GET.get(key, self._request.POST.get(key, None))

    def get_cookie(self, key):
        return self._request.COOKIES.get(key)
