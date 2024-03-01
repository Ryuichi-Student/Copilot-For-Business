from src.backend.utils.gpt import get_gpt_response
from textwrap import dedent
import json

class general_answer_gen:
    def __init__(self, answer: str, prompt: str, final_action_command: dict, action_commands: list[str], is_graph: bool): 
        self.answer = answer
        self.prompt = prompt
        self.final_action_command = final_action_command["command"] if (final_action_command and final_action_command["status"] == "success") else None
        self.action_commands = action_commands
        self.is_graph = is_graph
    
    def getAnswer(self) -> str:
        if self.is_graph:
            system_prompt = dedent('''\
            As an assistant, you are provided with a user question, accompanied by a graph that contains the necessary data to answer the query, as well as the action command and the sql query used to retrieve the data.
            Your task is to provide a precise and comprehensive answer to the user's question, utilizing the data points from the graph and the action command and sql query for explanation.
            The user has a strong grasp of graph data and seeks detailed insights from it. Structure your response by focusing on the following guidelines:
            - Directly present key data points. Avoid introductory phrases like "The data shows" or "Based on the data from this chart." Assume the user can readily understand the link between the graph and the data being discussed.
            - Concentrate exclusively on the data points to answer the user's question. Omit explanations of graphical elements or design—your responses should be rooted in the actual figures and numbers that address the inquiry.
            - Customize your answer to directly address the user's specific question, steering clear of any tangential or broad statements that do not directly support the answer.
            - Provide your answer is markdown format. Remember to add \ before any special characters if you don't want them to be formatted. E.g. add \$ so that it appears as $ rather than being formatted as a mathematical expression.
            - Detailed Explanation: Provide a explanation of how the answer is derived from the dataset, leveraging the action command and sql query to explain how the answer is derived. (do not include technical details about the database schema or the SQL)
                - For example, the sql query joins `total_amount_spent_on_orders_per_client` and `total_amount_spent_on_transactions_per_client` on `client_id` to get the total amount spent on orders and transactions per client, your explanation should be "the value for each client is calculated by summing the total amount spent on orders and transactions per client."
            \
                ''')
            user_prompt = dedent(f'''\
                Here is the user's question:
                {self.prompt}

                Here is the provided graph:
                {self.answer}
                
                Here are the intermediate action commands used to retrieve the data:
                {self.action_commands}

                Here is the final action command used to retrieve the data:
                {self.final_action_command}

                The graph is provided as an attachment. Please review the graph carefully to understand the data points and trends before responding to the user's question.
                \
            ''')
        else:
            system_prompt = dedent('''\
            As an assistant, you are provided with a user question, accompanied by a detailed dataset that contains the necessary information to answer the query. In addition, you have access to the action command and the sql query used to retrieve the data.
            Your task is to provide a precise and comprehensive answer to the user's question, utilizing the data points from the dataset and the action command and the sql query for further explanation of how the answer is derived.
            Your response should be constructed according to the following guidelines:
            - Direct Response with Data: When providing the answer to the user's query, accompany the full dataset with a direct statement that confirms the question has been answered. For instance, "Here is the complete list of client IDs as requested."
            - Complete Data Presentation: Ensure all requested figures, statistics, or query results are presented in totality, without omission or summarization.
            - Precision in Customization: Your answer should precisely cater to the user's specific question, presenting the data itself. Include every data point related to the query.
            - Provide your answer is markdown format. Remember to add \ before any special characters if you don't want them to be formatted. E.g. add \$ so that it appears as $ rather than being formatted as a mathematical expression.
             - Detailed Explanation: Provide a explanation of how the answer is derived from the dataset, leveraging the action command and sql query to explain how the answer is derived. (do not include technical details about the database schema or the SQL)
                - For example, the sql query joins `total_amount_spent_on_orders_per_client` and `total_amount_spent_on_transactions_per_client` on `client_id` to get the total amount spent on orders and transactions per client, your explanation should be "the value for each client is calculated by summing the total amount spent on orders and transactions per client."
\
            ''')

            user_prompt = dedent(f'''\
            Here is the user's question:
            {self.prompt}

            Here is the provided data:
            {self.answer}

            Here are the intermediate action commands used to retrieve the data:
            {self.action_commands}

            Here is the final action command used to retrieve the data:
            {self.final_action_command}

            Please review the data carefully to understand the key statistics and trends before responding to the user's question.
            \
            ''')
        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", user_prompt),
            top_p = 0.2
        )
        return gpt_response


    