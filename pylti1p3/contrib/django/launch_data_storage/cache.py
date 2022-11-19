from django.core.cache import caches  # type: ignore
from pylti1p3.launch_data_storage.cache import CacheDataStorage


class DjangoCacheDataStorage(CacheDataStorage):
    _cache = None

    def __init__(self, cache_name="default", **kwargs):
        self._cache = caches[cache_name]
        super().__init__(cache_name, **kwargs)
