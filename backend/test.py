# Use this if you want to test random functions
from backend.utils.gpt import get_gpt_response

def test():
    return "Backend is operational!"

def test_api(message_placeholder, prompt = "What is the capital of Japan?"):
    return get_gpt_response(
        ("system", "You are a helpful assistant"),
        ("user", prompt),
        stream=True,
        message_placeholder=message_placeholder
    )
