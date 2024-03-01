from src.backend.utils.gpt import get_gpt_response
from textwrap import dedent
from src.backend.database import Database
import json



def early_analysis(userQuery, db: Database):
    system_prompt = dedent('''\
        As a database analyst with expert knowledge in database schemas and SQL commands, your objective is to evaluate a specific user query against a given detailed database schema. Determine if the query can be directly answered by analyzing the schema or if executing SQL commands is essential to retrieve the required information. Your findings should be reported in a JSON format, structured as below:
        {
            "status": "<status>",
            "message": "<Your detailed analysis or guidance here>"
        }
        status: The status of the user query, which can be "schema" or "sql".
        message: A string in markdown that answers the user query based on the schema (when status is "schema") or is left empty (when status is "sql").
        If the status is "schema", it indicates that the query can be resolved by interpreting the schema itself. Please include in the message a detailed and insightful explanation that directly answers the user's query, leveraging the schema information.
            - When the user query are completely irrelevant to the database described by the schema and you think a different schema would be required to fulfill the request, the status should be "schema" and message should explain what about the user query is not included in the schema. Suggest in the message "did you choose the wrong database? If so, please choose the correct database to answer the query." wrapped in bold.
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