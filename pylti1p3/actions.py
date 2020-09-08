import typing as t

if t.TYPE_CHECKING:
    from typing_extensions import Final


class Action(object):
    OIDC_LOGIN = 'oidc_login'  # type: Final
    MESSAGE_LAUNCH = 'message_launch'  # type: Final
