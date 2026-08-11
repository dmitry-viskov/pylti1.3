from pylti1p3.exception import LineItemException
from pylti1p3.lineitem import LineItem
import json
import unittest


class TestLineItemInit(unittest.TestCase):
    def test_empty_init(self):
        li = LineItem()
        self.assertIsNone(li.get_id())
        self.assertIsNone(li.get_label())
        self.assertIsNone(li.get_score_maximum())
        self.assertIsNone(li.get_tag())

    def test_init_from_dict(self):
        li = LineItem(
            {
                "id": "http://lms.example.com/lineitems/1",
                "scoreMaximum": 100,
                "label": "Final Exam",
                "tag": "exam",
                "resourceId": "res-001",
                "resourceLinkId": "link-001",
            }
        )
        self.assertEqual(li.get_id(), "http://lms.example.com/lineitems/1")
        self.assertEqual(li.get_score_maximum(), 100)
        self.assertEqual(li.get_label(), "Final Exam")
        self.assertEqual(li.get_tag(), "exam")
        self.assertEqual(li.get_resource_id(), "res-001")
        self.assertEqual(li.get_resource_link_id(), "link-001")


class TestLineItemSetters(unittest.TestCase):
    def test_fluent_setters_return_self(self):
        li = LineItem()
        result = li.set_label("Quiz").set_score_maximum(50).set_tag("quiz")
        self.assertIs(result, li)

    def test_score_maximum_valid(self):
        li = LineItem().set_score_maximum(100)
        self.assertEqual(li.get_score_maximum(), 100)

    def test_score_maximum_zero_raises(self):
        with self.assertRaises(LineItemException):
            LineItem().set_score_maximum(0)

    def test_score_maximum_negative_raises(self):
        with self.assertRaises(LineItemException):
            LineItem().set_score_maximum(-10)

    def test_score_maximum_non_numeric_raises(self):
        with self.assertRaises(LineItemException):
            LineItem().set_score_maximum("high")

    def test_datetime_fields(self):
        li = LineItem().set_start_date_time("2024-01-01T00:00:00Z")
        li.set_end_date_time("2024-12-31T23:59:59Z")
        self.assertEqual(li.get_start_date_time(), "2024-01-01T00:00:00Z")
        self.assertEqual(li.get_end_date_time(), "2024-12-31T23:59:59Z")


class TestLineItemSubmissionReview(unittest.TestCase):
    def test_set_submission_review_minimal(self):
        li = LineItem().set_score_maximum(10)
        li.set_submission_review(["Completed"])
        sr = li.get_submission_review()
        self.assertEqual(sr["reviewableStatus"], ["Completed"])
        self.assertNotIn("label", sr)

    def test_set_submission_review_full(self):
        li = LineItem().set_score_maximum(10)
        li.set_submission_review(
            ["Completed", "InProgress"],
            label="Review here",
            url="https://tool.example.com/review",
            custom={"key": "val"},
        )
        sr = li.get_submission_review()
        self.assertEqual(sr["label"], "Review here")
        self.assertEqual(sr["url"], "https://tool.example.com/review")
        self.assertEqual(sr["custom"], {"key": "val"})

    def test_set_submission_review_invalid_status_raises(self):
        li = LineItem().set_score_maximum(10)
        with self.assertRaises(LineItemException):
            li.set_submission_review("Completed")


class TestLineItemGetValue(unittest.TestCase):
    def test_get_value_excludes_empty_fields(self):
        li = LineItem().set_score_maximum(50).set_label("Score")
        data = json.loads(li.get_value())
        self.assertEqual(data["scoreMaximum"], 50)
        self.assertEqual(data["label"], "Score")
        self.assertNotIn("id", data)
        self.assertNotIn("tag", data)

    def test_get_value_with_all_fields(self):
        li = (
            LineItem()
            .set_id("http://lms.example.com/lineitems/42")
            .set_score_maximum(100)
            .set_label("Midterm")
            .set_tag("midterm")
            .set_resource_id("r1")
            .set_resource_link_id("rl1")
            .set_start_date_time("2024-03-01T00:00:00Z")
            .set_end_date_time("2024-03-02T00:00:00Z")
        )
        data = json.loads(li.get_value())
        self.assertEqual(data["id"], "http://lms.example.com/lineitems/42")
        self.assertEqual(data["tag"], "midterm")
        self.assertEqual(data["startDateTime"], "2024-03-01T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
