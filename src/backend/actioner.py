from textwrap import dedent
from src.backend.utils.gpt import get_gpt_response

class Actioner:
    def __init__(self, *db_objects):
        self.db_objects = db_objects

    def get_requirements(self, query: str) -> list[str]:
        """
        Ask GPT for the data required to answer the query.
        :param query: str
        :return: list of str

        What products are most positively received by customers
        """
        system_prompt = dedent("""\
            You are a data consultant, giving advice to the user. You will be provided with a question regarding some data. Respond with a list of relevant information which would be required to answer the question. Limit the number of requirements to a maximum of 10. Please respond in a csv format including only the requirements and nothing else. Make sure commas are only used as delimiters and nowhere else.
             
            Here are two examples:
            
            User: "What is the average salary of a data scientist"
            Assistant: "historical salary data"
                               
            User: "Who is the most valuable customer"
            Assistant: "historical spending, future estimated spending, number of referrals and customer satisfaction"\
        """)
        response = get_gpt_response(
            ("system", system_prompt),
            ("user", query),
            top_p = 0.5, frequency_penalty = 0, presence_penalty = 0
        )
        return(response.split(','))

    def get_action(self, requirement: str, schema, query: str):
        pass


    class Action:
        """

        """