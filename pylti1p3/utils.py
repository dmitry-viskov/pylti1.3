import sys

if sys.version_info > (2, ):
    import urllib.parse as urlparse  # pylint: disable=no-name-in-module
    from urllib.parse import urlencode  # pylint: disable=no-name-in-module

    def encode_on_py3(arg, encoding):
        # type: (str, str) -> bytes
        return arg.encode(encoding)
else:
    import urlparse
    from urllib import urlencode  # pylint: disable=no-name-in-module,ungrouped-imports

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
