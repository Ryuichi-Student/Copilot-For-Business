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
        system_prompt = """
You are a data consultant, giving advice to the user. Try to answer questions directly. Here are two examples: 
If asked about the data required to answer question "What is the average salary of a data scientist", reply with historical salary data only.
For data to answer "Who is the most valuable customer", reply with historical spending, future estimated spending, number of referrals and customer satisfaction.
        """
        response = get_gpt_response(
            ("system", system_prompt),
            ("user", f'What information would be required to answer the following question: "{query}" Only state the most relevant ones.')
        )

        system_prompt = """
Only respond in the format: Requirement1, Requirement2, ... Do not write anything else and do not split the given requirements into smaller ones. 
For example, if asked to list down "The most useful requirements are years of experience, education level and salary amount", respond: "Years of experience, education level, salary amount".
If asked to list down "Location segmentation of health workers", respond "Location".
        """
        parsable_response = get_gpt_response(
            ("system", system_prompt),
            ("user", f'List down the data requirements listed by the user: "{response}"'),
            top_p=1, frequency_penalty=0, presence_penalty=0
        )

        # TODO: Choose which requirements can be fulfilled by the database

        return parsable_response.split(", ")

    def get_action(self, requirement: str, schema, query: str):
        pass


    class Action:
        """

        """