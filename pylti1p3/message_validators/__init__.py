from .deep_link import DeepLinkMessageValidator
from .resource_message import ResourceMessageValidator


def get_validators():
    return [DeepLinkMessageValidator(), ResourceMessageValidator()]
