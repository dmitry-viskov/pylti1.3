from pylti1p3.launch_data_storage.cache import CacheDataStorage


class Cache:
    _data = None

    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.get(key)

    def set(self, key, value, exp=None):  # pylint: disable=unused-argument
        self._data[key] = value


class FakeCacheDataStorage(CacheDataStorage):
    def __init__(self, *args, **kwargs):
        self._cache = Cache()
        super().__init__(*args, **kwargs)
