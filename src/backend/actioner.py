import json
from textwrap import dedent
from src.backend.utils.database import Database
from src.backend.utils.gpt import get_gpt_response

# https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683

class Actioner:
    def __init__(self, database):
        self._database = database

    @property
    def database(self) -> Database:
        return self._database
    
    def get_requirements(self, query: str) -> list[str]:
        """
        Ask GPT for the data required to answer the query.
        param query: str
        return: list[str]

        What products are most positively received by customers
        """
        system_prompt = dedent("""\
            You are a data consultant, giving advice to the user. You will be provided with a question regarding some data. Respond with a list of relevant information which would be required to answer the question. Limit the number of relevant information to a maximum of 10. Please respond in a csv format including only the requirements and nothing else. Make sure commas are only used as delimiters and nowhere else.
             
            Here are two examples:
            
            For the prompt "What is the average salary of a data scientist", reply with "historical data scientist salary data"
                               
            For the prompt "Who is the most valuable customer", reply with "historical customer spending, future estimated customer spending, number of referrals"\
        """)
        response = get_gpt_response(
            ("system", system_prompt),
            ("user", query)
        )
        return(response.split(','))

    def get_action(self, requirement: str, query: str):
        system_prompt = dedent("""\
            You are a data consultant, giving advice to the user. You will be provided with a database schema, some information which you will need to find, and the query which the information will be used to answer. Respond with details on how to find the request information, keeping in mind that the requested information will be used to solve the given query.
            
            First, determine whether it would be possible to find the information from the database. If not, respond with the following JSON object:
            
            {
                status: 'error',
                error: 'DATA_NOT_FOUND'
            }
            
            If it is possible, respond with a JSON object of the following structure, which will be used to generate SQL code to query the :
            
            {
                status: 'success',
                command: '',
                relevant_columns: [],
                graph_type: '',
                graph_info: {},
            }

            The 'command' field should contain a string detailing actionable steps in an imperative mood to find the required information. The 'relevant_columns' field should contain a JSON list of fields from the database which will be needed to generate SQL code to calculate the required information.
            
            The 'graph_type' field should contain a string of the name of the graph which should be used to best represent the required information. The 'graph_info' field should contain a JSON object providing details about the graph depending on which graph_type has been chosen. You may only choose from the following graph types and their corresponding graph_info:
            
            1. None
            This should be chosen when a graph is not suitable to represent the data. Choose this option when none of the other graphs from the list are suitable to represent the data. The following values for graph_type and graph_info should be used:
                graph_type: 'None'
                graph_info: {}
            
            2. Bar Chart
            This should be chosen when a bar chart is most suitbale to represent the data. The following values for graph_type and graph_info should be used. x_axis should contain a string of the column name that should be used as the x axis of the bar chart. y_axis should contain a string of the column name that should be used as the y axis of the bar chart:
                graph_type: 'Bar'
                graph_info: {
                    x_axis: '',
                    y_axis: '',
                }
        """)
        response = get_gpt_response(
            ("system", system_prompt),
            ("user", dedent(f'''\
                Here is the database schema:
                {self.database.textSchema}
                
                Provide details for finding {requirement} from the database. It will be used to answer the following question: {query}.
            ''')),
            jsonMode = True,
            top_p = 0.2
        )
        return response

    class Action:
        """

        """