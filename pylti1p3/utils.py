import sys

try:
    import urllib.parse as urlparse  # type: ignore
    from urllib.parse import urlencode  # type: ignore
except ImportError:  # python 2 fallback
    # pylint: disable=ungrouped-imports
    import urlparse  # type: ignore
    from urllib import urlencode  # type: ignore

if sys.version_info > (2, ):
    def encode_on_py3(arg, encoding):
        # type: (str, str) -> bytes
        return arg.encode(encoding)
else:
    def encode_on_py3(arg, encoding):
        # type: (str, str) -> bytes
        # pylint: disable=unused-argument
        return arg


def add_param_to_url(url, param_name, param_value):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query[str(param_name)] = str(param_value)

    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)
