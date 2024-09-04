from .hatchet import hatchet
from hatchet_sdk import Context
from .openai import create_completion
from .slack_client import slack_client
import logging

logger = logging.getLogger(__name__)

@hatchet.workflow(on_events=["general_response:start"])
class GeneralResponseAgentWorkflow():

    @hatchet.step()
    async def respond_to_general_inquiry(self, context: Context):
        logger.info("GeneralResponseAgentWorkflow: Starting response to general inquiry")
        workflow_input = context.workflow_input()
        message = workflow_input.get("message", "")
        channel = workflow_input.get("channel", "")
        logger.info(f"Received general inquiry in channel {channel}: '{message}'")

        logger.info("Generating response using OpenAI")
        response = await create_completion(
            prompt=f"""You are a helpful AI assistant. Respond to the following general inquiry or statement. Be polite, professional, and helpful. Provide information or assistance based on the context of the message.

User's message: "{message}"

Your response:""",
            max_tokens=300
        )

        logger.info(f"Generated response: '{response}'")

        logger.info("Sending response to Slack")
        await slack_client.send_message(channel, response)

        logger.info("GeneralResponseAgentWorkflow: Completed response to general inquiry")
        return {"response": response}
