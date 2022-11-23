import logging
import os

import openai

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


class GPT3:
    """GPT-3 service wrapper."""

    def __init__(self):
        """Sets API Key if available as environment variable."""
        if "OPENAI_API_KEY" not in os.environ:
            logger.critical(
                "OPENAI_API_KEY does not exist as environment variable.",
            )
            logger.debug(os.environ)
        self.api_key = os.getenv("OPENAI_API_KEY")

    def gpt3_request(self, prompt: str) -> str:
        """Sends request to GPT-3 service and returns response."""
        openai.api_key = self.api_key
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )
        logger.debug(f"{prompt} ... + {response}")
        return str(response.choices[0].text)
