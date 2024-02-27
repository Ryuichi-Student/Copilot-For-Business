from src.backend.utils.gpt import get_gpt_response
from textwrap import dedent
import json

class general_answer_gen:
    def __init__(self, answer: str, prompt: str, action_command: dict, query: str, is_graph: bool): 
        self.answer = answer
        self.prompt = prompt
        self.action_command = action_command["command"] if (action_command and action_command["status"] == "success") else None
        self.query = query
        self.is_graph = is_graph
    
    def getAnswer(self) -> str:
        if self.is_graph:
            system_prompt = dedent('''\
            As an assistant, you are tasked with analyzing a user query that comes with an accompanying graph displaying key data, alongside an action command and an SQL query that fetched this data. Your response must offer a precise and in-depth answer to the user's question, leveraging only the information depicted in the graph and elucidated through the action command and SQL query. The user possesses a proficient understanding of graph data and anticipates detailed insights drawn strictly from it. Tailor your response to meet these specific guidelines:
            Direct Presentation of Key Data Points: Commence your answer with the essential data points relevant to the user's question, directly engaging with the specifics. Given the user's adeptness at interpreting graph data, bypass introductory statements like "The data shows" or "Based on the data from this chart." Focus immediately on the figures and numbers within the graph that are crucial for answering the user's inquiry.
            Exclusive Focus on Relevant Data Points: Limit your response to the data points necessary to answer the user's question. Avoid discussions on graphical representation or design elements—your answer should hinge solely on the numbers and figures from the graph that directly resolve the query.
            Customization to the User's Specific Question: Ensure your response is finely tuned to the user's precise question, avoiding any deviation into generalized or irrelevant information that does not contribute directly to the query at hand.
            Detailed Explanation Based on Practical Application: Provide an in-depth explanation of how the answer is derived from the dataset, focusing on the practical application of the action command and SQL query. For example, if the SQL query merges data from total_amount_spent_on_orders_per_client and total_amount_spent_on_transactions_per_client through a client_id join to ascertain the total amount each client has spent on orders and transactions, explicitly state that "the aggregate value for each client is identified by adding their expenditures on orders and transactions, as evidenced by the joined datasets."
            Emphasize the practical steps taken to arrive at the answer, steering clear of theorizing about why these methods are effective. The goal is to elucidate the process of deriving the answer in a concrete manner, without delving into the rationale behind the data analysis technique or the theoretical underpinnings of the database schema or SQL itself.
            \
                ''')
            user_prompt = dedent(f'''\
                Here is the user's question:
                {self.prompt}

                Here is the provided graph:
                {self.answer}

                Here is the action command used to retrieve the data:
                {self.action_command}

                Here is the SQL query used to retrieve the data:
                {self.query}

                The graph is provided as an attachment. Please review the graph carefully to understand the data points and trends before responding to the user's question.
                \
            ''')
        else:
            system_prompt = dedent('''\
            As an assistant, you are equipped with a user query, accompanied by a comprehensive dataset that encompasses all necessary details for addressing the query. Additionally, you have access to the action command and the SQL query utilized for data retrieval.
            Your objective is to deliver an accurate and thorough response to the user's question, drawing upon the dataset's data points and employing the action command and SQL query to clarify the practical steps taken to derive the answer. Construct your response adhering to these tailored guidelines:
            Direct Response with Data: Begin your answer by affirming the user's question has been addressed, presenting the complete dataset or specific data points as required. For example, "Here is the complete list of client IDs as requested."
            Complete Data Presentation: Display all requested data, figures, statistics, or query results fully, without excluding or summarizing any details.
            Precision in Customization: Tailor your answer to fit the user's specific query precisely, focusing solely on presenting the relevant data. Incorporate every piece of data pertinent to the query.
            Detailed Practical Explanation: Offer a detailed account of how the answer was determined from the dataset, centering on the practical execution of the action command and SQL query. For instance, if an SQL query amalgamates total_amount_spent_on_orders_per_client and total_amount_spent_on_transactions_per_client via client_id to ascertain total expenditures on orders and transactions for each client, plainly state that "the overall expenditure for each client is determined by adding together their spending on orders and transactions, as indicated by the combined data."
            This approach emphasizes the concrete steps used to reach the conclusion, deliberately avoiding any discussion of the rationale behind the data analysis methods or the theoretical aspects of database schema or SQL itself.
            ''')

            user_prompt = dedent(f'''\
            Here is the user's question:
            {self.prompt}

            Here is the provided data:
            {self.answer}

            Here is the action command used to retrieve the data:
            {self.action_command}

            Here is the SQL query used to retrieve the data:
            {self.query}

            Please review the data carefully to understand the key statistics and trends before responding to the user's question.
            \
            ''')
        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", user_prompt),
            top_p = 0.2
        )
        return gpt_response


    