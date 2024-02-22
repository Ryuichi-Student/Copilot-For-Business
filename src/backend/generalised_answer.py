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
            As an assistant, it's crucial to directly answer the user's query with precision, drawing exclusively from the data provided. The user is adept at understanding data and is interested in the specifics of what the data reveals. Structure your response as follows:

            Highlight key data points from the provided data. Assume the connection between the data representation and its analysis is clear to the user.
            Focus your answer on the data points themselves. Stick to the raw facts and numbers that answer the user's question.
            Use a straightforward, conversational tone that speaks directly to the user's intelligence and familiarity with data analysis.
            Tailor your response to the user's specific inquiry, avoiding any digressions or generalized statements that don't directly contribute to the answer.
            Your aim is to furnish the user with a concise, informative response that relies entirely on the data points to provide a comprehensive answer to their question.
            \
            ''')

            user_prompt = dedent(f'''\
            Here is the user's question:
            {self.prompt}

            Here is the provided data:
            {dataframe_str}

            Please review the data carefully to understand the key statistics and trends before responding to the user's question.
            \
            ''')
        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", user_prompt),
            top_p = 0.2
        )
        return gpt_response


    