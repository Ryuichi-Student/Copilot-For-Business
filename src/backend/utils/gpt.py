import random
import time

from openai import OpenAI
import dotenv
import atexit
import tiktoken
import streamlit as st


# If .env exists, load the environment variables from it, otherwise load from environment
if dotenv.find_dotenv(".env"):
    config = dotenv.dotenv_values(".env")
    client = OpenAI(api_key=config['OPENAI_API_KEY'])
else:
    client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

def get_gpt_embedding(text):
    # calls openai embedding endpoint
    response = client.embeddings.create(
        input = text,
        model = "text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return embedding


total_tokens_used = 0


def track_tokens(func):
    """
    Decorator to track the number of tokens used by the GPT API.
    """
    def wrapper(*args, **kwargs):
        global total_tokens_used
        response, prompt_tokens, output_tokens = func(*args, **kwargs)
        total_tokens_used += prompt_tokens + output_tokens
        print(f"Prompt tokens: {prompt_tokens}, Output tokens: {output_tokens}, Total tokens used this session: {total_tokens_used}")
        return response
    return wrapper


@track_tokens
def get_gpt_response(*messages, history=None, gpt4=True, max_tokens=1500,
                     jsonMode=False, stream=False, message_placeholder=None,
                     top_p=0.5, frequency_penalty=0, presence_penalty=0):
    model = 'gpt-3.5-turbo-0125'
    if gpt4:
        model = 'gpt-4-turbo-preview'
        
    if history is None: history = []
    messages = history + [{"role": m[0], "content": m[1]} for m in messages]
    gpt_response = client.chat.completions.create( # type: ignore
        model = model,
        messages = messages,
        max_tokens = max_tokens,
        stream = stream,
        response_format = { 'type': 'json_object' if jsonMode else 'text' },
        top_p = top_p,
        frequency_penalty = frequency_penalty,
        presence_penalty = presence_penalty
    )
    if not stream:
        return gpt_response.choices[0].message.content, gpt_response.usage.prompt_tokens, gpt_response.usage.completion_tokens
    else:
        if message_placeholder is None:
            raise Exception("No stream placeholder!")

        response, output_tokens = get_stream(gpt_response, message_placeholder, "".join(history))
        prompt_tokens = num_tokens_from_string(" ".join(msg["content"] for msg in messages))
        return response, prompt_tokens, output_tokens


def get_stream(gpt_response, message_placeholder, full_response=""):
    tokens = 0
    for response in gpt_response:
        try:
            if response.choices[0].delta.content is None:
                continue
            delta = response.choices[0].delta.content
            full_response += delta
            tokens += num_tokens_from_string(delta)
            message_placeholder.markdown(full_response + "▌")
        except Exception as e:
            # print(response)
            print(f"error: {e}")
            continue
    message_placeholder.markdown(full_response)
    return full_response, tokens


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    # CLIP 100k base encoding is used by for the GPT-4 models
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


@atexit.register
def record_gpt_token_usage():
    """
    Records the total number of tokens used by the GPT API.
    """
    global total_tokens_used
    if total_tokens_used > 0:
        with open("gpt_token_usage.txt", "a") as f:
            f.write(f"{total_tokens_used}\n")

    with open("gpt_token_usage.txt", "r") as f:
        tokens = f.readlines()
        total = sum([int(token) for token in tokens])
        print(f"Total tokens used: {total}")
        print(f"Total tokens used this session: {total_tokens_used}")


def stream(text):
    x = ""
    tmp = []
    for letter in text:
        if random.random() < 0.2:
            tmp.append(x)
            x = ""
        x += letter
    tmp.append(x)
    x = ""
    for y in tmp:
        x += y
        yield x + " "
        time.sleep(0.05)