from pydantic import BaseModel
from typing import List, Optional

class SlackEventElement(BaseModel):
    type: str
    user: Optional[str] = None
    text: Optional[str] = None

class SlackEventRichTextSection(BaseModel):
    type: str
    elements: List[SlackEventElement]

class SlackEventBlock(BaseModel):
    type: str
    block_id: str
    elements: List[SlackEventRichTextSection]

class SlackEvent(BaseModel):
    user: str
    type: str
    ts: str
    client_msg_id: str
    text: str
    team: str
    blocks: List[SlackEventBlock]
    channel: str
    event_ts: str

class SlackEventRequest(BaseModel):
    type: str
    challenge: Optional[str] = None
    event: Optional[SlackEvent] = None