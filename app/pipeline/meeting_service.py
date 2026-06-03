import time

from app.pipeline.summarizer import generate_summary
from app.pipeline.extractor import (
    extract_action_items,
    extract_decisions
)

def analyze_meeting(transcript):

    start = time.time()

    summary = generate_summary(transcript)

    actions = extract_action_items(transcript)

    decisions = extract_decisions(transcript)

    end = time.time()

    return {
        "meeting_summary": summary,
        "action_items": actions,
        "key_decisions": decisions,
        "processing_time_seconds":
            round(end - start, 2)
    }