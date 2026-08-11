from pylti1p3.launch_data_storage.cache import CacheDataStorage


class FlaskCacheDataStorage(CacheDataStorage):
    _cache = None

    def __init__(self, cache, **kwargs):
        self._cache = cache
        super().__init__(cache, **kwargs)
