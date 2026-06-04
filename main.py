from fastapi import FastAPI, HTTPException
from app.schemas.request_schema import (
    TextRequest,
    MeetingRequest
)

from app.pipeline.prediction import generate_summary

# If using the new architecture
from app.pipeline.meeting_service import analyze_meeting

app = FastAPI(
    title="Meeting Intelligence Assistant",
    description="AI-powered Text Summarization and Meeting Intelligence API",
    version="2.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Meeting Intelligence Assistant Running Successfully",
        "version": "2.0.0"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/about")
def about():

    return {
        "project": "Meeting Intelligence Assistant",
        "features": [
            "Text Summarization",
            "Meeting Summarization",
            "Action Item Extraction",
            "Owner Identification",
            "Deadline Detection",
            "Decision Extraction"
        ]
    }


@app.post("/summarize")
def summarize(request: TextRequest):

    try:

        if not request.text.strip():

            raise HTTPException(
                status_code=400,
                detail="Input text cannot be empty"
            )

        summary = generate_summary(request.text)

        return {
            "status": "success",
            "original_text": request.text,
            "summary": summary
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/summarize-meeting")
def summarize_meeting(request: MeetingRequest):

    try:

        if not request.transcript.strip():

            raise HTTPException(
                status_code=400,
                detail="Transcript cannot be empty"
            )

        result = analyze_meeting(
            request.transcript
        )

        return {
            "status": "success",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
