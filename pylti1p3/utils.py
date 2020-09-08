import sys

if sys.version_info > (2, ):
    def encode_on_py3(arg, encoding):
        # type: (str, str) -> bytes
        return arg.encode(encoding)
else:
    def encode_on_py3(arg, encoding):
        # type: (str, str) -> bytes
        # pylint: disable=unused-argument
        return arg
