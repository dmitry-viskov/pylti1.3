import json
from unittest.mock import patch
import requests_mock
from .request import FakeRequest
from .tool_config import get_test_tool_conf
from .base import TestServicesBase


class TestCourseGroups(TestServicesBase):
    def test_course_groups(self):
        # pylint: disable=import-outside-toplevel
        from pylti1p3.contrib.flask import FlaskMessageLaunch

        tool_conf = get_test_tool_conf()

        with patch.object(
            FlaskMessageLaunch, "_get_jwt_body", autospec=True
        ) as get_jwt_body:
            message_launch = FlaskMessageLaunch(FakeRequest(), tool_conf)
            get_jwt_body.side_effect = lambda x: self._get_jwt_body()
            with patch("socket.gethostbyname", return_value="127.0.0.1"):
                with requests_mock.Mocker() as m:
                    m.post(
                        self._get_auth_token_url(),
                        text=json.dumps(self._get_auth_token_response()),
                    )

                    groups_data = [
                        {
                            "id": "44711f9f-64af-443a-bc3d-0abbfff73790",
                            "name": "Bob's Tuesday Group",
                            "set_id": "912cc53f-b431-447e-aff6-9d49aa9b72f2",
                            "tag": "marking",
                        },
                        {
                            "id": "bf2042b4-fdad-486a-86f3-bdb84e28a099",
                            "name": "Bob's Friday Group",
                            "set_id": "912cc53f-b431-447e-aff6-9d49aa9b72f2",
                            "tag": "marking",
                        },
                        {
                            "id": "f1cf534b-e45e-491b-bd65-f93741ef4d48",
                            "name": "Bob's Monday Group",
                            "set_id": "eaffdfa9-acfd-4f44-8c5e-36224ff81f5b",
                            "tag": "test",
                        },
                        {
                            "id": "89230b3-a341-447e-aff6-9d354aa9b72a6",
                            "name": "The cool kids group",
                        },
                    ]

                    groups_full_response = {
                        "id": self.context_groups_url,
                        "groups": groups_data,
                    }

                    sets_data = [
                        {
                            "id": "912cc53f-b431-447e-aff6-9d49aa9b72f2",
                            "name": "The Chemistry Lab Group Set",
                        },
                        {
                            "id": "eaffdfa9-acfd-4f44-8c5e-36224ff81f5b",
                            "name": "The Physics Lab Group Set",
                        },
                        {
                            "id": "02d133a7-d26e-41ec-8e63-c97fe562f0ca",
                            "name": "The Physics Lab Group Set 2",
                        },
                    ]

                    sets_with_groups_data = [
                        {
                            "id": "912cc53f-b431-447e-aff6-9d49aa9b72f2",
                            "name": "The Chemistry Lab Group Set",
                            "groups": [
                                {
                                    "id": "44711f9f-64af-443a-bc3d-0abbfff73790",
                                    "name": "Bob's Tuesday Group",
                                    "set_id": "912cc53f-b431-447e-aff6-9d49aa9b72f2",
                                    "tag": "marking",
                                },
                                {
                                    "id": "bf2042b4-fdad-486a-86f3-bdb84e28a099",
                                    "name": "Bob's Friday Group",
                                    "set_id": "912cc53f-b431-447e-aff6-9d49aa9b72f2",
                                    "tag": "marking",
                                },
                            ],
                        },
                        {
                            "id": "eaffdfa9-acfd-4f44-8c5e-36224ff81f5b",
                            "name": "The Physics Lab Group Set",
                            "groups": [
                                {
                                    "id": "f1cf534b-e45e-491b-bd65-f93741ef4d48",
                                    "name": "Bob's Monday Group",
                                    "set_id": "eaffdfa9-acfd-4f44-8c5e-36224ff81f5b",
                                    "tag": "test",
                                }
                            ],
                        },
                        {
                            "id": "02d133a7-d26e-41ec-8e63-c97fe562f0ca",
                            "name": "The Physics Lab Group Set 2",
                            "groups": [],
                        },
                    ]

                    sets_full_response = {
                        "id": self.context_group_sets_url,
                        "sets": sets_data,
                    }

                    m.get(
                        self.context_groups_url, text=json.dumps(groups_full_response)
                    )
                    m.get(
                        self.context_group_sets_url, text=json.dumps(sets_full_response)
                    )

                    message_launch = message_launch.validate_registration()
                    self.assertTrue(message_launch.has_cgs())

                    cgs = message_launch.get_cgs()
                    groups = cgs.get_groups()
                    self.assertEqual(groups, groups_data)

                    self.assertTrue(cgs.has_sets())

                    sets = cgs.get_sets()
                    self.assertEqual(sets, sets_data)

                    sets_with_groups = cgs.get_sets(include_groups=True)
                    self.assertEqual(sets_with_groups, sets_with_groups_data)
