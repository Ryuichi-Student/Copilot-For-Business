from openai import OpenAI
import dotenv

config = dotenv.dotenv_values(".env")
client = OpenAI(api_key=config['OPENAI_API_KEY'])

def get_gpt_embedding(text):
    # calls openai embedding endpoint
    response = client.embeddings.create(
        input = text,
        model = "text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return embedding

def get_gpt_response(*messages, history=None, model="gpt-4-1106-preview", max_tokens=1500,
                     jsonMode=False, stream=False, message_placeholder=None,
                     top_p=0.5, frequency_penalty=0, presence_penalty=0):
    if history is None: history = []
    messages = history + [{"role": m[0], "content": m[1]} for m in messages]
    gpt_response = client.chat.completions.create(
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
        return gpt_response.choices[0].message.content
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