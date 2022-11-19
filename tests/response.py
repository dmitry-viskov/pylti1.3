class FakeResponse:
    data = None
    cookies = None

    def __init__(self, data):
        self.data = data
        self.cookies = {}

    def set_cookie(self, name, value, **kwargs):
        self.cookies[name] = {
            "value": value,
        }
        self.cookies[name].update(kwargs)

    def get_cookies_dict(self):
        return {key: cookie["value"] for key, cookie in self.cookies.items()}
