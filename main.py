from fastapi import FastAPI, HTTPException
from app.schemas.request_schema import TextRequest
from app.pipeline.prediction import generate_summary

app = FastAPI(
    title="AI Text Summarizer",
    description="Production Grade NLP Summarization API",
    version="1.0"
)


@app.get("/")
def home():

    return {
        "message": "AI Text Summarizer Running Successfully"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/summarize")
def summarize(request: TextRequest):

    try:

        summary = generate_summary(request.text)

        return {
            "original_text": request.text,
            "summary": summary
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )