from src.backend.utils.gpt import get_gpt_response
from textwrap import dedent
import json

class general_answer_gen:
    def __init__(self, answer: str, prompt: str):
        self.answer = answer
        self.prompt = prompt
    
    def getAnswer(self) -> str:
        system_prompt = dedent('''\
        As an assistant, it's crucial to directly answer the user's query with precision, drawing exclusively from the data provided. The user is adept at understanding graph data and is interested in the specifics of what the data reveals. Structure your response as follows:

Highlight key data points without prefacing your statements with phrases like "The data shows" or "Based on the data from this chart." Assume the connection between the graph and the data is clear to the user.
Focus your answer on the data points themselves. There's no need to explain the graphical elements or design—stick to the raw facts and numbers that answer the user's question.
Use a straightforward, conversational tone that speaks directly to the user's intelligence and familiarity with data analysis. Think of it as sharing insights with a colleague who has equal expertise.
Tailor your response to the user's specific inquiry, avoiding any digressions or generalized statements that don't directly contribute to the answer.
Your aim is to furnish the user with a concise, informative response that relies entirely on the data points to provide a comprehensive answer to their question.
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
        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", user_prompt),
            top_p = 0.2
        )
        return gpt_response


    