import logging
import os

import uvicorn
from fastapi import FastAPI, Response
from hatchet_sdk import Hatchet
from pydantic import BaseModel

from src.config import settings
from ..models.slack_event import SlackEventRequest


from slack_sdk import WebClient

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hatchet Quickstart API. Use /slack/events to post Slack events."}


@app.post("/slack/events")
async def slack_events(slack_event: SlackEventRequest):
    logger.info(f"Received Slack event: type={slack_event.type}")
    
    if slack_event.type == "url_verification":
        logger.info("Responding to URL verification challenge")
        return {"challenge": slack_event.challenge}

    if slack_event.type == "event_callback" and slack_event.event:
        await hatchet.client.admin.aio.run_workflow("OrchestratorWorkflow", slack_event.event.model_dump())

    logger.info("Slack event processing completed")
    return Response(status_code=200)

def start():
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)