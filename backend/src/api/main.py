import json
import logging
import os
from typing import AsyncGenerator, Optional
import asyncio

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from hatchet_sdk import Hatchet
from pydantic import BaseModel

from src.config import settings
from ..models.slack_event import SlackEventRequest, SlackEvent


# Add Slack-specific imports
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the environment variable for Hatchet
os.environ["HATCHET_CLIENT_TOKEN"] = settings.hatchet_client_token

# Initialize Hatchet client
hatchet = Hatchet()

# Initialize Slack client
slack_client = WebClient(token=settings.slack_bot_token)

# Initialize FastAPI app
app = FastAPI()

# Define CORS origins
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Define Pydantic model for response
class ScrapeResponse(BaseModel):
    messageId: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/slack/events")
async def slack_events(slack_event: SlackEventRequest):
    logger.info(f"Received Slack event: type={slack_event.type}")
    
    if slack_event.type == "url_verification":
        logger.info("Responding to URL verification challenge")
        return {"challenge": slack_event.challenge}

    if slack_event.type == "event_callback" and slack_event.event:
        event_id = f"{slack_event.event_id}_{slack_event.event.event_ts}"
        logger.info(f"Processing event: id={event_id}")
        
        # Deduplicate events
        async with events_lock:
            if event_id in processed_events:
                logger.info(f"Duplicate event received: {event_id}")
                return Response(status_code=200)
            
            processed_events.add(event_id)
            logger.info(f"Added event to processed set. Total processed: {len(processed_events)}")
            
            if len(processed_events) > 1000:
                processed_events.pop()
                logger.info("Removed oldest event from processed set")

        # Trigger the Hatchet orchestrator workflow
        logger.info(f"Triggering OrchestratorWorkflow for event: {event_id}")
        await hatchet.client.admin.aio.run_workflow("OrchestratorWorkflow", slack_event.event.model_dump())

    logger.info("Slack event processing completed")
    return Response(status_code=200)

def start():
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)