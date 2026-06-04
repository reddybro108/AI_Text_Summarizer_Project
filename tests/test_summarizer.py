import importlib
import sys
import types
import unittest
from unittest.mock import patch


class FakeSummarizer:
    def __init__(self, response=None, should_raise=False):
        self.response = response or [{"summary_text": "Mock summary"}]
        self.should_raise = should_raise
        self.calls = []

    def __call__(self, text, max_length, min_length, do_sample):
        self.calls.append(
            {
                "text": text,
                "max_length": max_length,
                "min_length": min_length,
                "do_sample": do_sample,
            }
        )

        if self.should_raise:
            raise RuntimeError("pipeline failed")

        return self.response


def load_prediction_module(fake_summarizer):
    fake_transformers = types.ModuleType("transformers")
    pipeline_calls = []

    def fake_pipeline(*args, **kwargs):
        pipeline_calls.append({"args": args, "kwargs": kwargs})
        return fake_summarizer

    fake_transformers.pipeline = fake_pipeline

    with patch.dict(sys.modules, {"transformers": fake_transformers}):
        sys.modules.pop("app.pipeline.summary_backend", None)
        sys.modules.pop("app.pipeline.prediction", None)
        module = importlib.import_module("app.pipeline.prediction")

    return module, pipeline_calls


class SummarizerTests(unittest.TestCase):
    def test_generate_summary_returns_model_output(self):
        fake_summarizer = FakeSummarizer()
        prediction, pipeline_calls = load_prediction_module(fake_summarizer)

        result = prediction.generate_summary("This is a long transcript.")

        self.assertEqual(result, "Mock summary")
        self.assertEqual(len(pipeline_calls), 1)
        self.assertEqual(pipeline_calls[0]["kwargs"]["task"], "summarization")
        self.assertEqual(
            pipeline_calls[0]["kwargs"]["model"],
            "sshleifer/distilbart-cnn-12-6",
        )
        self.assertEqual(len(fake_summarizer.calls), 1)
        self.assertEqual(fake_summarizer.calls[0]["text"], "This is a long transcript.")

    def test_generate_summary_chunks_long_transcript(self):
        fake_summarizer = FakeSummarizer()
        prediction, _ = load_prediction_module(fake_summarizer)

        long_text = " ".join(["word"] * 2000)
        result = prediction.generate_summary(long_text)

        self.assertEqual(result, "Mock summary")
        self.assertGreater(len(fake_summarizer.calls), 1)

    def test_generate_summary_returns_empty_message_for_blank_input(self):
        fake_summarizer = FakeSummarizer()
        prediction, _ = load_prediction_module(fake_summarizer)

        result = prediction.generate_summary("   ")

        self.assertEqual(result, "Input text is empty")
        self.assertEqual(len(fake_summarizer.calls), 0)

    def test_generate_summary_returns_error_message_on_failure(self):
        fake_summarizer = FakeSummarizer(should_raise=True)
        prediction, _ = load_prediction_module(fake_summarizer)

        result = prediction.generate_summary("This is a long transcript.")

        self.assertTrue(result)
        self.assertNotEqual(result, "Input text is empty")


if __name__ == "__main__":
    unittest.main()
