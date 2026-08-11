import json
import unittest
from datetime import datetime
from pylti1p3.grade import Grade
from pylti1p3.exception import LtiException


class TestGradeModel(unittest.TestCase):
    def test_fluent_setters_return_self(self):
        g = Grade()
        result = g.set_score_given(80).set_score_maximum(100).set_user_id("u1")
        self.assertIs(result, g)

    def test_score_given_valid(self):
        g = Grade().set_score_given(75.5)
        self.assertEqual(g.get_score_given(), 75.5)

    def test_score_given_zero_is_valid(self):
        g = Grade().set_score_given(0)
        self.assertEqual(g.get_score_given(), 0)

    def test_score_given_negative_raises(self):
        with self.assertRaises(LtiException):
            Grade().set_score_given(-1)

    def test_score_given_non_numeric_raises(self):
        with self.assertRaises(LtiException):
            Grade().set_score_given("high")

    def test_score_maximum_valid(self):
        g = Grade().set_score_maximum(100)
        self.assertEqual(g.get_score_maximum(), 100)

    def test_score_maximum_negative_raises(self):
        with self.assertRaises(LtiException):
            Grade().set_score_maximum(-5)

    def test_timestamp_from_string(self):
        g = Grade().set_timestamp("2024-01-15T10:00:00+00:00")
        self.assertEqual(g.get_timestamp(), "2024-01-15T10:00:00+00:00")

    def test_timestamp_from_datetime(self):
        dt = datetime(2024, 6, 1, 12, 0, 0)
        g = Grade().set_timestamp(dt)
        self.assertEqual(g.get_timestamp(), "2024-06-01T12:00:00")

    def test_get_value_excludes_none_fields(self):
        g = Grade().set_score_given(80).set_score_maximum(100).set_user_id("u1")
        data = json.loads(g.get_value())
        self.assertEqual(data["scoreGiven"], 80)
        self.assertEqual(data["scoreMaximum"], 100)
        self.assertEqual(data["userId"], "u1")
        self.assertNotIn("comment", data)
        self.assertNotIn("timestamp", data)

    def test_get_value_includes_submission_when_started_at_set(self):
        g = Grade().set_started_at("2024-01-01T09:00:00")
        data = json.loads(g.get_value())
        self.assertIn("submission", data)
        self.assertEqual(data["submission"]["startedAt"], "2024-01-01T09:00:00")

    def test_get_value_includes_submission_when_submitted_at_set(self):
        g = Grade().set_submitted_at("2024-01-01T10:00:00")
        data = json.loads(g.get_value())
        self.assertIn("submission", data)
        self.assertEqual(data["submission"]["submittedAt"], "2024-01-01T10:00:00")

    def test_get_value_no_submission_when_neither_set(self):
        g = Grade().set_score_given(50).set_score_maximum(100)
        data = json.loads(g.get_value())
        self.assertNotIn("submission", data)

    def test_extra_claims_merged_in_get_value(self):
        g = Grade().set_score_given(10).set_score_maximum(20)
        g.set_extra_claims({"customField": "customValue"})
        data = json.loads(g.get_value())
        self.assertEqual(data["customField"], "customValue")

    def test_comment(self):
        g = Grade().set_comment("Well done!")
        self.assertEqual(g.get_comment(), "Well done!")

    def test_activity_and_grading_progress(self):
        g = (
            Grade()
            .set_activity_progress("Completed")
            .set_grading_progress("FullyGraded")
        )
        self.assertEqual(g.get_activity_progress(), "Completed")
        self.assertEqual(g.get_grading_progress(), "FullyGraded")


if __name__ == "__main__":
    unittest.main()
