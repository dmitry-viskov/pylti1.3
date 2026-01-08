from .deep_link import DeepLinkMessageValidator
from .resource_message import ResourceMessageValidator
from .privacy_launch import PrivacyLaunchValidator
from .submission_review import SubmissionReviewLaunchValidator


def get_validators():
    return [
        DeepLinkMessageValidator(),
        ResourceMessageValidator(),
        PrivacyLaunchValidator(),
        SubmissionReviewLaunchValidator(),
    ]
