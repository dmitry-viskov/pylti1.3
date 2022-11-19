import unittest
from pylti1p3.utils import add_param_to_url


class TestUtils(unittest.TestCase):
    def test_add_param_to_url(self):
        res = add_param_to_url(
            "https://lms.example.com/class/2923/groups/sets", "user_id", 123
        )
        self.assertEqual(
            res, "https://lms.example.com/class/2923/groups/sets?user_id=123"
        )

        res = add_param_to_url(
            "https://lms.example.com/class/2923/groups/sets?some=xxx", "user_id", 123
        )
        self.assertIn(
            res,
            [
                "https://lms.example.com/class/2923/groups/sets?some=xxx&user_id=123",
                "https://lms.example.com/class/2923/groups/sets?user_id=123&some=xxx",
            ],
        )

        res = add_param_to_url(
            "https://lms.example.com/class/2923/groups/sets?user_id=456", "user_id", 123
        )
        self.assertEqual(
            res, "https://lms.example.com/class/2923/groups/sets?user_id=123"
        )
