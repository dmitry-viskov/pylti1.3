from .session import FakeSession


class FakeRequest:
    GET = {}
    POST = {}
    COOKIES = {}
    session = None
    secure = False

    def __init__(self, get=None, post=None, cookies=None, session=None, secure=False):
        self.GET = get if get else {}
        self.POST = post if post else {}
        self.COOKIES = cookies if cookies else {}
        self.session = session if session else FakeSession()
        self.secure = secure

    def is_secure(self):
        return self.secure
