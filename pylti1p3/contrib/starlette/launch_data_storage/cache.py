import asyncio
from aiocache import Cache
from pylti1p3.launch_data_storage.cache import CacheDataStorage


class StarletteCacheDataStorage(CacheDataStorage):

    def __init__(self, cache: Cache, **kwargs):
        self._cache = cache
        super().__init__(cache, **kwargs)
        self._loop = asyncio.new_event_loop()

    def get_value(self, key):
        key = self._prepare_key(key)
        return self._loop.run_until_complete(self._cache.get(key))

    def set_value(self, key, value, exp=None):
        key = self._prepare_key(key)
        self._loop.run_until_complete(self._cache.set(key, value, exp))

    def check_value(self, key):
        key = self._prepare_key(key)
        return self._loop.run_until_complete(self._cache.exists(key))

    def can_set_keys_expiration(self):
        return True

    def set_request(self, request):
        super().set_request(request)

    def get_session_id(self):
        return super().get_session_id()

    def set_session_id(self, session_id):
        super().set_session_id(session_id)

    def remove_session_id(self):
        super().remove_session_id()
