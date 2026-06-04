from __future__ import annotations

import logging
from functools import lru_cache

from transformers import pipeline

logger = logging.getLogger(__name__)


def _simple_extractive_summary(text: str, max_sentences: int = 3) -> str:
    sentences = [
        sentence.strip()
        for sentence in text.replace("\n", " ").split(".")
        if sentence.strip()
    ]

    if not sentences:
        return text.strip()

    return ". ".join(sentences[:max_sentences]).strip() + ("." if len(sentences[:max_sentences]) else "")


@lru_cache(maxsize=1)
def get_summarization_pipeline(model_name: str):
    logger.info("Loading summarization model: %s", model_name)
    try:
        return pipeline(task="summarization", model=model_name)
    except Exception as exc:
        logger.warning(
            "Falling back to offline summarizer because the model could not be loaded: %s",
            exc,
        )
        return None


def summarize_text(
    text: str,
    *,
    model_name: str,
    max_length: int,
    min_length: int,
) -> str:
    cleaned_text = text.strip()
    if not cleaned_text:
        return "Input text is empty"

    summarizer = get_summarization_pipeline(model_name)

    if summarizer is None:
        return _simple_extractive_summary(cleaned_text)

    try:
        result = summarizer(
            cleaned_text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )

        if result and result[0].get("summary_text"):
            return result[0]["summary_text"].strip()

        return _simple_extractive_summary(cleaned_text)
    except Exception as exc:
        logger.error("Summarization Error: %s", exc)
        return _simple_extractive_summary(cleaned_text)
