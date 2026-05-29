from transformers import pipeline
import logging

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

        # Validate empty input
        if not text.strip():

            return "Input text is empty"

        # Generate summary
        summary = summarizer(
            text,
            max_length=120,
            min_length=30,
            do_sample=False
        )

        # Return summarized text
        return summary[0]["summary_text"]

    except Exception as e:

        logger.error(f"Summarization Error: {e}")

        return f"Error occurred: {str(e)}"