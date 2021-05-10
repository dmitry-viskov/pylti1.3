from .deep_link import DeepLinkMessageValidator
from .resource_message import ResourceMessageValidator
from .privacy_launch import PrivacyLaunchValidator


def get_validators():
    return [
        DeepLinkMessageValidator(),
        ResourceMessageValidator(),
        PrivacyLaunchValidator(),
    ]
