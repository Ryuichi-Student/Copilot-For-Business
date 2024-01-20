import openai
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

def get_gpt_response(system, prompt, model = "gpt-4-1106-preview", max_tokens = 1500):
    gpt_response = openai.ChatCompletion.create(
        model = model,
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        max_tokens = max_tokens
    )
    return gpt_response["choices"][0]["message"]["content"]