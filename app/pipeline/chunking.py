from __future__ import annotations

import re
from typing import Callable, List


def split_text_into_chunks(text: str, max_words: int = 400) -> List[str]:
    cleaned_text = text.strip()

    if not cleaned_text:
        return []

    overlap_words = min(60, max(0, max_words - 1))
    stride = max(1, max_words - overlap_words) if overlap_words else max_words

    sentences = re.split(r"(?<=[.!?])\s+|\n+", cleaned_text)
    chunks: List[str] = []
    current_words: List[str] = []

    def flush_current() -> None:
        nonlocal current_words

        if current_words:
            chunks.append(" ".join(current_words).strip())

            if overlap_words:
                current_words = current_words[-overlap_words:]
            else:
                current_words = []

    def add_segment(words: List[str]) -> None:
        if not words:
            return

        for start in range(0, len(words), stride):
            segment = words[start : start + max_words]

            if segment:
                chunks.append(" ".join(segment).strip())

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        words = sentence.split()

        if len(words) > max_words:
            if current_words:
                flush_current()

            add_segment(words)

            if overlap_words:
                current_words = words[-overlap_words:]
            continue

        if current_words and len(current_words) + len(words) > max_words:
            flush_current()

        current_words.extend(words)

    flush_current()

    return chunks


def summarize_with_chunking(
    text: str,
    summarizer: Callable[..., list],
    *,
    max_words: int = 400,
    max_length: int = 120,
    min_length: int = 30,
) -> str:
    cleaned_text = text.strip()

    if not cleaned_text:
        return "Input text is empty"

    chunks = split_text_into_chunks(cleaned_text, max_words=max_words)

    if not chunks:
        return "Input text is empty"

    chunk_summaries: List[str] = []

    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )

        if result and result[0].get("summary_text"):
            chunk_summaries.append(result[0]["summary_text"].strip())

    if not chunk_summaries:
        return "Unable to generate summary"

    if len(chunk_summaries) == 1:
        return chunk_summaries[0]

    combined_summary = " ".join(chunk_summaries)
    final_result = summarizer(
        combined_summary,
        max_length=max_length,
        min_length=min_length,
        do_sample=False,
    )

    if final_result and final_result[0].get("summary_text"):
        return final_result[0]["summary_text"].strip()

    return combined_summary
