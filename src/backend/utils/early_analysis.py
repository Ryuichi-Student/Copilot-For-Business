from src.backend.utils.gpt import get_gpt_response
from textwrap import dedent
from src.backend.database import Database
import json



def early_analysis(userQuery, db: Database):
    system_prompt = dedent('''\
        Imagine you're a highly skilled database analyst with a deep understanding of database schemas and SQL commands. You're presented with a user query alongside a detailed database schema. 
        Your task is to meticulously analyze whether the user's query can be answered directly based on the provided schema or if it requires the execution of one or more SQL commands to retrieve the necessary information.
        Your response should be formatted as a JSON object as follows:
        {
            "status": "schema" or "sql",
            "message": "Your message here"
        }
        If the status is "schema", it indicates that the query can be resolved by interpreting the schema itself. Please include in the message a detailed and insightful explanation that directly answers the user's query, leveraging the schema information.
        If the status is "sql", it suggests that the query necessitates the execution of SQL commands to obtain the answer, leave the message empty.
    ''')

    user_prompt = dedent(f'''\
        User Query: {userQuery}
        Database Schema: {db.getTextSchema()}
    ''')

    response = get_gpt_response(
        ("system", system_prompt),
        ("user",  user_prompt),
        jsonMode=True,
        top_p=0.2,
    ) 
    response_json = json.loads(response)
    return response_json