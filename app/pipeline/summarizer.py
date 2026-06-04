from app.pipeline.chunking import summarize_with_chunking
from app.pipeline.summary_backend import summarize_text

def generate_summary(text):

    return summarize_with_chunking(
        text,
        lambda chunk, **_: [
            {
                "summary_text": summarize_text(
                    chunk,
                    model_name="facebook/bart-large-cnn",
                    max_length=150,
                    min_length=40,
                )
            }
        ],
        max_words=400,
        max_length=150,
        min_length=40
    )
