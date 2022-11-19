import json
from unittest.mock import patch
import requests_mock
from .request import FakeRequest
from .tool_config import get_test_tool_conf
from .base import TestServicesBase


class TestNamesRolesProvisioningService(TestServicesBase):
    def test_get_members(self):
        # pylint: disable=import-outside-toplevel
        from pylti1p3.contrib.django import DjangoMessageLaunch

        tool_conf = get_test_tool_conf()

        with patch.object(
            DjangoMessageLaunch, "_get_jwt_body", autospec=True
        ) as get_jwt_body:
            message_launch = DjangoMessageLaunch(FakeRequest(), tool_conf)
            get_jwt_body.side_effect = lambda x: self._get_jwt_body()
            with patch("socket.gethostbyname", return_value="127.0.0.1"):
                with requests_mock.Mocker() as m:
                    m.post(
                        self._get_auth_token_url(),
                        text=json.dumps(self._get_auth_token_response()),
                    )
                    m.get(
                        self._get_jwt_body()[
                            "https://purl.imsglobal.org/spec/lti-nrps/claim/namesroleservice"
                        ]["context_memberships_url"],
                        text=json.dumps(
                            {
                                "members": [
                                    {
                                        "status": "Active",
                                        "user_id": "20eb59f5-26e8-46bc-87b0-57ed54820aeb",
                                        "roles": [
                                            "http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"
                                        ],
                                    }
                                ],
                                "id": "http://canvas.docker/api/lti/courses/1/names_and_roles",
                                "context": {
                                    "title": "Test",
                                    "id": "4dde05e8ca1973bcca9bffc13e1548820eee93a3",
                                    "label": "Test",
                                },
                            }
                        ),
                        headers={
                            "Status": "200 OK",
                            "X-Request-Context-Id": "fb3662e8-527c-4c83-b4d5-b32d247a896c",
                            "X-XSS-Protection": "1; mode=block",
                            "X-Content-Type-Options": "nosniff",
                            "Transfer-Encoding": "chunked",
                            "X-Rate-Limit-Remaining": "600.0",
                            "X-Runtime": "0.235817",
                            "Server": "nginx/1.13.5",
                            "X-Canvas-Meta": "o=lti/ims/names_and_roles;n=course_index;t=Course;i=1;b=892132;"
                            "m=892132;u=0.08;y=0.00;d=0.01;",
                            "Connection": "keep-alive",
                            "ETag": 'W/"a198e0b4e31245287ba175ddf5a9223c"',
                            "X-Request-Cost": "0.09043669500000007",
                            "X-UA-Compatible": "IE=Edge,chrome=1",
                            "Cache-Control": "max-age=0, private, must-revalidate",
                            "Date": "Mon, 12 Aug 2019 09:50:45 GMT",
                            "Link": "<http://canvas.docker/api/lti/courses/1/names_and_roles?page=1"
                            '&per_page=10>; rel="current",<http://canvas.docker/api/lti/cou'
                            'rses/1/names_and_roles?page=1&per_page=10>; rel="first",'
                            "<http://canvas.docker/api/lti/courses/1/names_and_roles"
                            '?page=1&per_page=10>; rel="last"',
                            "X-Frame-Options": "SAMEORIGIN",
                            "Content-Type": "application/vnd.ims.lti-nrps.v2.membershipcontainer+json; charset=utf-8",
                        },
                    )
                    members = (
                        message_launch.validate_registration().get_nrps().get_members()
                    )
                    self.assertEqual(len(members), 1)
                    self.assertDictEqual(
                        members[0],
                        {
                            "status": "Active",
                            "user_id": "20eb59f5-26e8-46bc-87b0-57ed54820aeb",
                            "roles": [
                                "http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"
                            ],
                        },
                    )
