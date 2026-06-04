import logging

from app.pipeline.chunking import summarize_with_chunking
from app.pipeline.summary_backend import summarize_text

# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def generate_summary(text: str):

    try:
        return summarize_with_chunking(
            text,
            lambda chunk, **_: [
                {
                    "summary_text": summarize_text(
                        chunk,
                        model_name="sshleifer/distilbart-cnn-12-6",
                        max_length=120,
                        min_length=30,
                    )
                }
            ],
            max_words=400,
            max_length=120,
            min_length=30
        )

    except Exception as e:

        logger.error(f"Summarization Error: {e}")

        return f"Error occurred: {str(e)}"
