try:
    from collections.abc import MutableMapping
except ImportError:
    # Python 2.7
    from collections import MutableMapping


class FakeSession(MutableMapping):
    def __init__(self, *args, **kwargs):
        # pylint: disable=super-init-not-called
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key
