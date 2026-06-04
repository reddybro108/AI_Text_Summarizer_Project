from transformers import pipeline
import re

from app.pipeline.chunking import summarize_with_chunking

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)


def extract_action_items(text):

    action_items = []

    sentences = re.split(r'[.!?]\s*', text)

    keywords = [
        "action item",
        "todo",
        "task",
        "follow up",
        "follow-up",
        "complete",
        "deliver",
        "implement",
        "deploy"
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        for keyword in keywords:

            if keyword.lower() in sentence.lower():

                action_items.append(sentence)
                break

    return action_items


def extract_decisions(text):

    decisions = []

    sentences = re.split(r'[.!?]\s*', text)

    keywords = [
        "decided",
        "decision",
        "approved",
        "agreed",
        "finalized",
        "accepted"
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        for keyword in keywords:

            if keyword.lower() in sentence.lower():

                decisions.append(sentence)
                break

    return decisions


def extract_owners_and_deadlines(text):

    results = []

    sentences = re.split(r'[.!?]\s*', text)

    deadline_patterns = [
        r'by\s+\w+',
        r'before\s+\w+',
        r'on\s+\d+\s+\w+',
        r'next\s+\w+'
    ]

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        owner = None
        deadline = None

        words = sentence.split()

        if len(words) > 0:
            owner = words[0]

        for pattern in deadline_patterns:

            match = re.search(pattern, sentence, re.IGNORECASE)

            if match:
                deadline = match.group()
                break

        if owner and deadline:

            results.append({
                "owner": owner,
                "task": sentence,
                "deadline": deadline
            })

    return results


def summarize_meeting(transcript):

    return {
        "meeting_summary": summarize_with_chunking(
            transcript,
            summarizer,
            max_words=400,
            max_length=150,
            min_length=40
        ),
        "action_items": extract_action_items(transcript),
        "key_decisions": extract_decisions(transcript),
        "owners_and_deadlines": extract_owners_and_deadlines(transcript)
    }
