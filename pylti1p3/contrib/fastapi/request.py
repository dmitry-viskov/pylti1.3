from pylti1p3.request import Request


class FastAPIRequest(Request):
    _request = None
    _form_data = None

    def __init__(self, request, form_data):
        """
        Parameters:
            request: FastAPI request
            form_data: form data from FastAPI request
                To get form data from FastAPI request, must use async method.
                As we don't use async functions here, form data must be provided from outside.
        """

        super().__init__()

        self._request = request
        self._form_data = form_data

    @property
    def session(self):
        return self._request.session

    def get_param(self, key):
        if self._request.method == "GET":
            return self._request.query_params.get(key, None)
        return self._form_data.get(key)

    def get_cookie(self, key):
        return self._request.cookies.get(key, None)

    def is_secure(self):
        return self._request.url.is_secure
