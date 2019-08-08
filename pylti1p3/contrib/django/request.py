from pylti1p3.request import Request


class DjangoRequest(Request):
    _request = None

    def __init__(self, request):
        self.set_request(request)

    def set_request(self, request):
        self._request = request

    def get_param(self, key):
        return self._request.GET.get(key, self._request.POST.get(key, None))

    def get_cookie(self, key):
        return self._request.COOKIES.get(key)
