from pylti1p3.lineitem import LineItem
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.exception import LtiException
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestDeepLinkResourceDefaults(unittest.TestCase):
    def test_default_type_is_lti_resource_link(self):
        self.assertEqual(DeepLinkResource().get_type(), "ltiResourceLink")

    def test_default_target_is_iframe(self):
        self.assertEqual(DeepLinkResource().get_target(), "iframe")

    def test_defaults_are_none(self):
        r = DeepLinkResource()
        self.assertIsNone(r.get_title())
        self.assertIsNone(r.get_url())
        self.assertIsNone(r.get_lineitem())
        self.assertIsNone(r.get_icon_url())
        self.assertIsNone(r.get_html())

    def test_default_custom_params_is_empty(self):
        self.assertEqual(DeepLinkResource().get_custom_params(), {})


class TestDeepLinkResourceFluentSetters(unittest.TestCase):
    def test_set_title_returns_self(self):
        r = DeepLinkResource()
        self.assertIs(r.set_title("My Tool"), r)

    def test_chaining(self):
        r = (
            DeepLinkResource()
            .set_title("Quiz")
            .set_url("https://tool.example.com/quiz/1")
            .set_target("window")
        )
        self.assertEqual(r.get_title(), "Quiz")
        self.assertEqual(r.get_url(), "https://tool.example.com/quiz/1")
        self.assertEqual(r.get_target(), "window")


class TestDeepLinkResourceToDict(unittest.TestCase):
    def test_to_dict_minimal(self):
        r = DeepLinkResource().set_title("T").set_url("https://example.com")
        d = r.to_dict()
        self.assertEqual(d["type"], "ltiResourceLink")
        self.assertEqual(d["title"], "T")
        self.assertEqual(d["url"], "https://example.com")
        self.assertNotIn("lineItem", d)
        self.assertNotIn("icon", d)
        self.assertNotIn("custom", d)
        self.assertNotIn("html", d)

    def test_to_dict_html(self):
        r = DeepLinkResource().set_type("html").set_html("<div>Test Element</div>")
        d = r.to_dict()
        self.assertEqual(d["html"], "<div>Test Element</div>")

    def test_to_dict_html_no_content(self):
        r = DeepLinkResource().set_type("html")
        with self.assertRaises(LtiException):
            r.to_dict()

    def test_to_dict_link_html(self):
        r = DeepLinkResource().set_type("link").set_html("<div>Test Element</div>")
        d = r.to_dict()
        self.assertEqual(d["embed"], {"html": "<div>Test Element</div>"})

    def test_to_dict_with_icon_url(self):
        r = DeepLinkResource().set_icon_url("https://example.com/icon.png")
        d = r.to_dict()
        self.assertEqual(d["icon"], {"url": "https://example.com/icon.png"})

    def test_to_dict_with_custom_params(self):
        r = DeepLinkResource().set_custom_params({"chapter": "3"})
        d = r.to_dict()
        self.assertEqual(d["custom"], {"chapter": "3"})

    def test_to_dict_with_lineitem_score_maximum_only(self):
        li = LineItem().set_score_maximum(100)
        r = DeepLinkResource().set_lineitem(li)
        d = r.to_dict()
        self.assertIn("lineItem", d)
        self.assertEqual(d["lineItem"]["scoreMaximum"], 100)
        self.assertNotIn("label", d["lineItem"])
        self.assertNotIn("tag", d["lineItem"])

    def test_to_dict_with_lineitem_full(self):
        li = (
            LineItem()
            .set_score_maximum(50)
            .set_label("Score")
            .set_tag("quiz")
            .set_resource_id("res-001")
        )
        r = DeepLinkResource().set_lineitem(li)
        d = r.to_dict()
        li_dict = d["lineItem"]
        self.assertEqual(li_dict["scoreMaximum"], 50)
        self.assertEqual(li_dict["label"], "Score")
        self.assertEqual(li_dict["tag"], "quiz")
        self.assertEqual(li_dict["resourceId"], "res-001")

    def test_to_dict_with_lineitem_submission_review(self):
        li = LineItem().set_score_maximum(10)
        li.set_submission_review(["Completed"], label="Review")
        r = DeepLinkResource().set_lineitem(li)
        d = r.to_dict()
        self.assertIn("submissionReview", d["lineItem"])
        self.assertEqual(d["lineItem"]["submissionReview"]["label"], "Review")


if __name__ == "__main__":
    unittest.main()
