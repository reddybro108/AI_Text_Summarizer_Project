import re
import spacy

nlp = spacy.load("en_core_web_sm")

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