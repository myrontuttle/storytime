from typing import Optional

import logging
import os
import sys

import openai

logging.basicConfig(
    filename="logfile.log",
    stream=sys.stdout,
    filemode="w",
    format="{asctime} | {levelname} | {message}",
    level=logging.INFO,
)


def apikey() -> Optional[str]:
    """Returns API Key if available as environment variable."""
    if "OPENAI_API_KEY" not in os.environ:
        logging.critical(
            "OPENAI_API_KEY does not exist as environment variable.",
        )
        logging.debug(os.environ)
        return None
    return os.getenv("OPENAI_API_KEY")


def gpt3_request(api_key: str, prompt: str) -> str:
    """Sends request to GPT-3 service and returns response."""
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.1,
        max_tokens=5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    logging.debug(f"{prompt} ... + {response}")
    return str(response.choices[0].text)
