from src.backend.utils.gpt import get_gpt_response
from textwrap import dedent
import json

class general_answer_gen:
    def __init__(self, answer: str, prompt: str, is_graph: bool):
        self.answer = answer
        self.prompt = prompt
        self.is_graph = is_graph
    
    def getAnswer(self) -> str:
        if self.is_graph:
            system_prompt = dedent('''\
            As an assistant, ensure your response to the user's query is direct and precise, using only the data provided. The user has a strong grasp of graph data and seeks detailed insights from it. Structure your response by focusing on the following guidelines:

Directly present key data points. Avoid introductory phrases like "The data shows" or "Based on the data from this chart." Assume the user can readily understand the link between the graph and the data being discussed.
Concentrate exclusively on the data points to answer the user's question. Omit explanations of graphical elements or design—your responses should be rooted in the actual figures and numbers that address the inquiry.
Employ a straightforward, conversational tone that acknowledges the user's intelligence and data analysis proficiency. Approach the conversation as if you're exchanging insights with a peer who possesses equivalent expertise.
Customize your answer to directly address the user's specific question, steering clear of any tangential or broad statements that do not directly support the answer.
Aim to provide a concise, informative response that leverages the data points to deliver a thorough answer to the user's question, without assuming the need to explain or highlight graph visualization aspects.
Your objective is to equip the user with precise, data-driven insights, relying solely on the data points for a comprehensive understanding of their query.
            \
                ''')
            user_prompt = dedent(f'''\
                Here is the user's question:
                {self.prompt}

                Here is the provided graph:
                {self.answer}

                The graph is provided as an attachment. Please review the graph carefully to understand the data points and trends before responding to the user's question.
                \
            ''')
        else:
            system_prompt = dedent('''\
            As an assistant, your role is to respond to the user's query with precision and directness, utilizing the data at hand. The user possesses advanced knowledge in database management and is in pursuit of in-depth insights. Your response should be constructed according to the following guidelines:
            Direct Response with Data: When providing the answer to the user's query, accompany the full dataset with a direct statement that confirms the question has been answered. For instance, "Here is the complete list of client IDs as requested."
            Complete Data Presentation: Ensure all requested figures, statistics, or query results are presented in totality, without omission or summarization.
            Data-Focused Communication: Use a straightforward conversational tone that acknowledges the user's expertise, directly outputting data as you would with a colleague of equal knowledge.
            Precision in Customization: Your answer should precisely cater to the user's specific question, presenting the data itself. Include every data point related to the query.
            Clear Data Layout: Display the data clearly in its original form, straight from the database query. This includes full listings and comprehensive tables.
            Objective: Equip the user with exact, unfiltered data, basing your response solely on the provided database information or specific values for an all-encompassing answer to their query. Combine the raw data output with a direct acknowledgment that the user's question has been answered.
\
            ''')

            user_prompt = dedent(f'''\
            Here is the user's question:
            {self.prompt}

            Here is the provided data:
            {self.answer}

            Please review the data carefully to understand the key statistics and trends before responding to the user's question.
            \
            ''')
        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", user_prompt),
            top_p = 0.2
        )
        return gpt_response


    