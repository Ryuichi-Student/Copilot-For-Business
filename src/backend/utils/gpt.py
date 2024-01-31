try:
    import openai
except ImportError as e:
    print(e)
    print(e.path)
import dotenv

config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

def get_gpt_embedding(text):
    # calls openai embedding endpoint
    response = openai.Embedding.create(
        input = text,
        model = "text-embedding-ada-002"
    )
    embedding = response['data'][0]['embedding']
    return embedding

def get_gpt_response(*messages, history=None, model="gpt-4-1106-preview", max_tokens=1500,
                     stream=False, message_placeholder=None):
    if history is None: history = []
    messages = history + [{"role": m[0], "content": m[1]} for m in messages]
    gpt_response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        stream=stream
    )
    if not stream:
        return gpt_response["choices"][0]["message"]["content"]
    else:
        if message_placeholder is None:
            raise Exception("No stream placeholder!")
        return get_stream(gpt_response, message_placeholder, "".join(history))

def get_stream(gpt_response, message_placeholder, full_response=""):
    for response in gpt_response:
        try:
            full_response += "" if not response.choices[0].delta else response.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌")
        except Exception as e:
            print(f"error: {e}")
            continue
    message_placeholder.markdown(full_response)
    return full_response