from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

class MeetingRequest(BaseModel):
    transcript: str