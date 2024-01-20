# Use this if you want to test random functions
from backend.utils.gpt import get_gpt_response

def test():
    return "Backend is operational!"

def test_api(prompt = "What is the capital of Japan?"):
    return get_gpt_response("You are a helpful assistant", prompt)
