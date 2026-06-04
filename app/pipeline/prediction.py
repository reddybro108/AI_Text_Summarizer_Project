from transformers import pipeline
import logging

from app.pipeline.chunking import summarize_with_chunking

# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Load summarization pipeline
logger.info("Loading summarization model...")

summarizer = pipeline(
    task="summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

logger.info("Model loaded successfully")


def generate_summary(text: str):

    try:
        return summarize_with_chunking(
            text,
            summarizer,
            max_words=400,
            max_length=120,
            min_length=30
        )

    except Exception as e:

        logger.error(f"Summarization Error: {e}")

        return f"Error occurred: {str(e)}"
