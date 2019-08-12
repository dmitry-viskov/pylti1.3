class DjangoFakeRequest(object):
    GET = {}
    POST = {}
    COOKIES = {}
    session = {}

    def __init__(self, get=None, post=None, cookies=None, session=None):
        self.GET = get if get else {}
        self.POST = post if post else {}
        self.COOKIES = cookies if cookies else {}
        self.session = session if session else {}
