from ..models.slack_event import SlackEvent
from .hatchet import hatchet
from hatchet_sdk import Context
from .openai import create_completion
import logging

logger = logging.getLogger(__name__)

# Define the orchestrator workflow using Hatchet's decorator
@hatchet.workflow(on_events=["orchestrator:start"])
class OrchestratorWorkflow():

    @hatchet.step()
    async def analyze_message(self, context: Context):
        logger.info("OrchestratorWorkflow: Starting message analysis")
        # Convert the workflow input to a SlackEvent object
        slack_event = SlackEvent(**context.workflow_input())
        logger.info(f"Received Slack event: user={slack_event.user}, channel={slack_event.channel}, text='{slack_event.text}'")
        
        # Use OpenAI to classify the intent of the message
        intent = await create_completion(
            prompt=f"""Analyze the following message and determine if it's related to scheduling a meeting or if it's a general inquiry/statement.

Message: "{slack_event.text}"

Respond with only one word:
- 'meeting' if the message is clearly about scheduling a meeting.
- 'general' for any other type of inquiry or statement.

Your response:"""
        )
        logger.info(f"OpenAI classified intent as: {intent}")
        
        # Spawn the appropriate workflow based on the intent
        if intent.lower().strip() == "meeting":
            logger.info("Spawning MeetingPlanningAgentWorkflow")
            await context.aio.spawn_workflow("MeetingPlanningAgentWorkflow", {
                "message": slack_event.text,
                "channel": slack_event.channel
            })
        else:
            logger.info("Spawning GeneralResponseAgentWorkflow")
            await context.aio.spawn_workflow("GeneralResponseAgentWorkflow", {
                "message": slack_event.text,
                "channel": slack_event.channel
            })
        logger.info("OrchestratorWorkflow: Message analysis and workflow spawning completed")
