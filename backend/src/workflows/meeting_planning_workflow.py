from .hatchet import hatchet
from hatchet_sdk import Context
from .openai import create_completion
from .slack_client import slack_client
import logging

logger = logging.getLogger(__name__)

# Define the meeting planning workflow
@hatchet.workflow(on_events=["meeting_planning:start"])
class MeetingPlanningAgentWorkflow():

    @hatchet.step()
    async def respond_to_meeting_inquiry(self, context: Context):
        logger.info("MeetingPlanningAgentWorkflow: Starting response to meeting inquiry")
        workflow_input = context.workflow_input()
        message = workflow_input.get("message", "")
        channel = workflow_input.get("channel", "")
        logger.info(f"Received meeting inquiry in channel {channel}: '{message}'")

        # Generate response using OpenAI
        response = await create_completion(
            prompt=f"""You are a helpful meeting assistant. Respond to the following meeting-related inquiry or statement. Be polite, professional, and helpful. Don't actually schedule a meeting, but pretend you're assisting with the process.

User's message: "{message}"

Your response:""",
            max_tokens=300
        )

        logger.info(f"Generated response: '{response}'")

        # Send the response back to Slack
        await slack_client.send_message(channel, response)

        logger.info("MeetingPlanningAgentWorkflow: Completed response to meeting inquiry")
        return {"response": response}