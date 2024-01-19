import openai
import dotenv

config = dotenv.dotenv_values("backend/.env")
openai.api_key = config['OPENAI_API_KEY']
embedding_model = "text-embedding-ada-002"

def get_gpt_embedding(text):
    # calls openai embedding endpoint
    response = openai.Embedding.create(
        input=text,
        model=embedding_model
    )
    embedding = response['data'][0]['embedding'] # type: ignore
    return embedding

def get_gpt_response(prompts, model="gpt-4-1106-preview", max_tokens = 1000):
    gpt_response = openai.ChatCompletion.create(model=model,
                                                    messages=prompts,
                                                    max_tokens=max_tokens)
    print(gpt_response)
    return gpt_response["choices"][0]["message"]["content"]