from pydantic import BaseModel
from typing import List

class ActionItem(BaseModel):
    owner: str
    task: str
    deadline: str

class MeetingResponse(BaseModel):
    meeting_summary: str
    action_items: List[ActionItem]
    key_decisions: List[str]
    processing_time_seconds: float