import json
import re

from fastapi import FastAPI, HTTPException, Request

from app.schemas.request_schema import TextRequest

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


def _extract_transcript_from_request_body(raw_body: bytes) -> str:
    body_text = raw_body.decode("utf-8", errors="replace").strip()

    if not body_text:
        return ""

    try:
        parsed = json.loads(body_text)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, dict):
        transcript = parsed.get("transcript", "")
        return transcript if isinstance(transcript, str) else str(transcript)

    if isinstance(parsed, str):
        return parsed

    if not body_text.startswith("{"):
        return body_text

    match = re.search(r'"transcript"\s*:\s*"(.*)"\s*}\s*$', body_text, re.S)
    if match:
        return match.group(1).strip()

    return body_text


@app.post("/summarize-meeting")
async def summarize_meeting(request: Request):

    try:
        raw_body = await request.body()
        transcript = _extract_transcript_from_request_body(raw_body)

        if not transcript.strip():

            raise HTTPException(
                status_code=400,
                detail="Transcript cannot be empty"
            )

        result = analyze_meeting(
            transcript
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
