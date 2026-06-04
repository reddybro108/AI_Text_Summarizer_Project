from transformers import pipeline

from app.pipeline.chunking import summarize_with_chunking

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_summary(text):

    return summarize_with_chunking(
        text,
        summarizer,
        max_words=400,
        max_length=150,
        min_length=40
    )
