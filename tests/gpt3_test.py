import logging

from storytime.gpt3 import gpt3_request

logging.basicConfig(
    format="{asctime} | {levelname} | {message}",
    level=logging.INFO,
)


def test_request_gpt3():
    """Test GPT-3 API."""
    prompt = "Once upon a time"
    response = gpt3_request(prompt)
    logging.info(
        f"{prompt} ... + {response}",
    )
    assert response
