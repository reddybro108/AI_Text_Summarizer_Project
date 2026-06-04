import re

try:
    import spacy
except ModuleNotFoundError:  # pragma: no cover - environment fallback
    spacy = None


class _FallbackDoc:
    def __init__(self):
        self.ents = []


class _FallbackNLP:
    def __call__(self, text):
        return _FallbackDoc()


def load_nlp():
    if spacy is None:
        return _FallbackNLP()

    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # Keep the API alive even if the full model is unavailable.
        return spacy.blank("en")


nlp = load_nlp()

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

def extract_action_items(text):

    results = []

    sentences = re.split(r"[.!?]", text)

    for sentence in sentences:

        sentence = sentence.strip()

        if "will" not in sentence.lower():
            continue

        doc = nlp(sentence)

        owner = ""

        for ent in doc.ents:

            if ent.label_ == "PERSON":
                owner = ent.text
                break

        deadline = ""

        for day in DAYS:

            if day.lower() in sentence.lower():
                deadline = day
                break

        results.append(
            {
                "owner": owner,
                "task": sentence,
                "deadline": deadline
            }
        )

    return results


def extract_decisions(text):

    decisions = []

    sentences = re.split(r"[.!?]", text)

    keywords = [
        "decided",
        "approved",
        "agreed",
        "finalized"
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        for keyword in keywords:

            if keyword in sentence.lower():

                decisions.append(sentence)
                break

    return decisions
