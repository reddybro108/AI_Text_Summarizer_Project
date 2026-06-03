import importlib
import sys
import types
import unittest
from unittest.mock import patch


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
        elif "Bob" in text:
            ents.append(FakeEntity("Bob", "PERSON"))
        return FakeDoc(ents)


class BlankNLP:
    def __call__(self, text):
        return FakeDoc([])


def load_extractor_module(spacy_load_side_effect=None):
    fake_spacy = types.ModuleType("spacy")

    if spacy_load_side_effect is None:
        fake_spacy.load = lambda name: FakeNLP()
    elif isinstance(spacy_load_side_effect, BaseException):
        def raise_missing_model(name):
            raise spacy_load_side_effect

        fake_spacy.load = raise_missing_model
    else:
        fake_spacy.load = spacy_load_side_effect

    fake_spacy.blank = lambda lang: BlankNLP()

    with patch.dict(sys.modules, {"spacy": fake_spacy}):
        sys.modules.pop("app.pipeline.extractor", None)
        module = importlib.import_module("app.pipeline.extractor")

    return module


class ExtractorTests(unittest.TestCase):
    def test_extract_action_items_detects_owner_and_deadline(self):
        extractor = load_extractor_module()

        result = extractor.extract_action_items(
            "Alice will follow up on the budget by Monday. The team will review it."
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["owner"], "Alice")
        self.assertEqual(result[0]["deadline"], "Monday")
        self.assertIn("follow up on the budget", result[0]["task"])

    def test_extract_decisions_finds_keywords(self):
        extractor = load_extractor_module()

        result = extractor.extract_decisions(
            "The team decided to proceed. We also agreed on the timeline."
        )

        self.assertEqual(
            result,
            [
                "The team decided to proceed",
                "We also agreed on the timeline",
            ],
        )

    def test_extract_action_items_uses_blank_fallback_when_model_is_missing(self):
        extractor = load_extractor_module(
            spacy_load_side_effect=OSError("missing model")
        )

        result = extractor.extract_action_items(
            "Alice will prepare the launch plan by Friday."
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["owner"], "")
        self.assertEqual(result[0]["deadline"], "Friday")


if __name__ == "__main__":
    unittest.main()
