from storytime.gpt3 import apikey, gpt3_request


def test_request_gpt3():
    """Test GPT-3 API."""
    api_key = apikey()
    if api_key:
        prompt = "Once upon a time"
        response = gpt3_request(api_key, prompt)
    else:
        response = " there was a kingdom far, far away."
    assert response
