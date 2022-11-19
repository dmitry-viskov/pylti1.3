from ..exception import LtiException
from .abstract import MessageValidatorAbstract


class SubmissionReviewLaunchValidator(MessageValidatorAbstract):
    """Validates the body of a LTI submission review launch.

    The launch must include a for_user claim specifying the user
    who's submission is being reviewed, as well as the line item
    for the reviewed submission.
    """

    def validate(self, jwt_body) -> bool:
        self.run_common_validators(jwt_body)

        if "https://purl.imsglobal.org/spec/lti-ags/claim/endpoint" not in jwt_body:
            raise LtiException(
                "Grade services must be included in a LtiSubmissionReviewRequest"
            )

        ags_endpoint_claim = jwt_body[
            "https://purl.imsglobal.org/spec/lti-ags/claim/endpoint"
        ]
        if "lineitem" not in ags_endpoint_claim:
            raise LtiException(
                "A LtiSubmissionReviewRequest must specify the lineitem it was launched for"
            )

        for_user_claim = jwt_body.get(
            "https://purl.imsglobal.org/spec/lti/claim/for_user"
        )
        if for_user_claim is None:
            raise LtiException(
                "For user claim must be included in a LtiSubmissionReviewRequest"
            )
        if "user_id" not in for_user_claim:
            raise LtiException("For user claim must include user_id")

        return True

    def can_validate(self, jwt_body) -> bool:
        return (
            jwt_body.get("https://purl.imsglobal.org/spec/lti/claim/message_type")
            == "LtiSubmissionReviewRequest"
        )
