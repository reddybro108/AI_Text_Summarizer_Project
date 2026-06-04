import importlib
import sys
import types
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient


class FakeSummarizer:
    def __call__(self, text, max_length, min_length, do_sample):
        return [{"summary_text": f"Summary: {text[:20]}"}]


class FakeEntity:
    def __init__(self, text, label_):
        self.text = text
        self.label_ = label_


class FakeDoc:
    def __init__(self, ents=None):
        self.ents = ents or []


class FakeNLP:
    def __call__(self, text):
        ents = []
        if "Alice" in text:
            ents.append(FakeEntity("Alice", "PERSON"))
        return FakeDoc(ents)


def load_main_module():
    fake_transformers = types.ModuleType("transformers")
    fake_transformers.pipeline = lambda *args, **kwargs: FakeSummarizer()

    fake_spacy = types.ModuleType("spacy")
    fake_spacy.load = lambda name: FakeNLP()
    fake_spacy.blank = lambda lang: FakeNLP()

    with patch.dict(sys.modules, {"transformers": fake_transformers, "spacy": fake_spacy}):
        for module_name in [
            "app.pipeline.prediction",
            "app.pipeline.extractor",
            "app.pipeline.meeting_service",
            "main",
        ]:
            sys.modules.pop(module_name, None)

        module = importlib.import_module("main")

    return module


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.main = load_main_module()
        cls.client = TestClient(cls.main.app)

    def test_root_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "message": "Meeting Intelligence Assistant Running Successfully",
                "version": "2.0.0",
            },
        )

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_about_endpoint(self):
        response = self.client.get("/about")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Meeting Summarization", response.json()["features"])

    def test_summarize_endpoint_returns_summary(self):
        response = self.client.post("/summarize", json={"text": "This is a meeting transcript."})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["original_text"], "This is a meeting transcript.")
        self.assertTrue(payload["summary"].startswith("Summary:"))

    def test_summarize_endpoint_handles_long_transcript(self):
        long_text = " ".join(["word"] * 2000)
        response = self.client.post("/summarize", json={"text": long_text})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "success")
        self.assertTrue(payload["summary"].startswith("Summary:"))

    def test_summarize_endpoint_rejects_blank_text(self):
        response = self.client.post("/summarize", json={"text": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Input text cannot be empty")

    def test_summarize_meeting_endpoint_returns_structured_data(self):
        response = self.client.post(
            "/summarize-meeting",
            json={"transcript": "Alice will send the notes by Friday. The team decided to proceed."},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["data"]["key_decisions"], ["The team decided to proceed"])
        self.assertEqual(payload["data"]["action_items"][0]["owner"], "Alice")
        self.assertEqual(payload["data"]["action_items"][0]["deadline"], "Friday")

    def test_summarize_meeting_endpoint_handles_long_transcript(self):
        long_transcript = " ".join(["word"] * 1990) + " Alice will send the notes by Friday. The team decided to proceed."
        response = self.client.post(
            "/summarize-meeting",
            json={"transcript": long_transcript},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "success")
        self.assertGreaterEqual(len(payload["data"]["action_items"]), 1)
        self.assertGreaterEqual(len(payload["data"]["key_decisions"]), 1)

    def test_summarize_meeting_endpoint_accepts_multiline_json_like_body(self):
        raw_body = (
            '{\n'
            '  "transcript": "James Miller: Good morning everyone. The purpose of today\'s meeting is to review the progress of Project Atlas.\n\n'
            'Sarah Johnson: The first production release is expected by Friday.\n\n'
            'Alice will send the notes by Friday. The recommendation engine should be completed by Tuesday."\n'
            '}'
        )

        response = self.client.post(
            "/summarize-meeting",
            content=raw_body,
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "success")
        self.assertGreaterEqual(len(payload["data"]["action_items"]), 1)

    def test_summarize_meeting_endpoint_rejects_blank_transcript(self):
        response = self.client.post("/summarize-meeting", json={"transcript": ""})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Transcript cannot be empty")


if __name__ == "__main__":
    unittest.main()
