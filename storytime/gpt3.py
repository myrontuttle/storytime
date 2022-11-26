from typing import Optional

import logging
import os

import openai

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def get_api_key_from_env() -> Optional[str]:
    """Returns API Key if available as environment variable."""
    if "OPENAI_API_KEY" not in os.environ:
        logger.critical(
            "OPENAI_API_KEY does not exist as environment variable.",
        )
        logger.debug(os.environ)
    return os.getenv("OPENAI_API_KEY")


def generate_text(
    prompt: str,
    temp: Optional[float] = 0.8,
    max_tokens: Optional[int] = 1256,
    top_p: Optional[float] = 1,
) -> str:
    """Sends request to GPT-3 Completion service and returns response."""
    openai.api_key = get_api_key_from_env()
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=temp,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"],
        )
        return response["choices"][0]["text"]
    except Exception as e:
        logger.error(e)
        logger.debug(
            f" from: {prompt} with temp: {temp}, "
            f" max_tokens: {max_tokens}, and top_p: {top_p}"
        )
        return ""


def generate_image(prompt: str) -> str:
    """Sends request to GPT-3 Image service and returns response."""
    openai.api_key = get_api_key_from_env()
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        return response["data"][0]["url"]
    except Exception as e:
        logger.error(e)
        logger.debug(f" from: {prompt}")
        return ""
