from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class SlackClient:
    def __init__(self):
        self.client = AsyncWebClient(token=settings.slack_bot_token)
        logger.info("Slack client initialized")

    async def send_message(self, channel: str, text: str):
        logger.info(f"Attempting to send message to Slack channel: {channel}")
        try:
            result = await self.client.chat_postMessage(
                channel=channel,
                text=text
            )
            logger.info(f"Message successfully sent to Slack. Timestamp: {result['ts']}")
            return result
        except SlackApiError as e:
            logger.error(f"Error sending message to Slack: {e}")
            raise

slack_client = SlackClient()
logger.info("Slack client singleton created")
