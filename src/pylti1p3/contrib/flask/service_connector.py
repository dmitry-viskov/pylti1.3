import typing as t
from datetime import datetime, timedelta
from pylti1p3.service_connector import ServiceConnector


class FlaskServiceConnector(ServiceConnector):
    access_tokens: t.Dict[str, tuple[str, datetime]]
    access_tokens = {}

    def _get_cached_access_token(self, scope_key: str) -> t.Union[str, None]:
        cached_token = self.__class__.access_tokens.get(scope_key)
        if cached_token is not None:
            token, expires = cached_token
            if expires > datetime.now():
                return token

        return None

    def _cache_access_token(self, scope_key: str, access_token: str, expires_in: float):
        self.__class__.access_tokens[scope_key] = (
            access_token,
            datetime.now() + timedelta(seconds=expires_in),
        )
