import openai
from ..config import settings
import logging

logger = logging.getLogger(__name__)

openai.api_key = settings.openai_api_key
logger.info("OpenAI API key set")

async def create_completion(prompt, model="gpt-3.5-turbo-instruct", max_tokens=300):
    logger.info(f"Sending request to OpenAI. Model: {model}, Max tokens: {max_tokens}")
    logger.debug(f"Prompt: {prompt}")
    try:
        response = await openai.Completion.acreate(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        logger.info("Received response from OpenAI")
        logger.debug(f"Full response: {response}")
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {e}")
        raise