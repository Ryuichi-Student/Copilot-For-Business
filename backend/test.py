# Use this if you want to test random functions
from backend.LLM_utils import get_gpt_response

def test():
    return "Backend is operational!"

def test_api(prompt="What is the capital of Japan?"):
    return get_gpt_response(
        [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    )
