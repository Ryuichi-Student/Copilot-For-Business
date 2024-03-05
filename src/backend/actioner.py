import json
from typing import List, Dict, Any, Union
from textwrap import dedent
from src.backend.database import Database
from src.backend.utils.gpt import get_gpt_response
from src.backend.visualisation import visualisation_subclasses

class Actioner:
    def __init__(self, database):
        self._database = database

    @property
    def database(self) -> Database:
        return self._database
    
    def get_requirements(self, query: str) -> Dict[str, Union[List[str], str]]:
        system_prompt = dedent("""\
            You are a data consultant, giving advice to the user. You will be provided with a question regarding some data stored in a database. The database schema will be provided.

            Respond with a list of datapoints required to answer the question. Datapoints should include all data required to answer the question and should have a common axis. Limit the number of datapoints to a maximum of 10. If the question can be directly answered from the data in the database, reply with a single datapoint.
            
            Respond with the following JSON object.
            {
                "requirements": []
                "axis": ""
            }

            The "requirements" field should contain a list of string, each one corresponding with one of the datapoints.
                               
            The "axis" field should contain the name of a common axis for which the requirements should be joined upon.
                               
            Make sure the "axis" field is NOT included as one of the requirements.

            Answer in a consistent style.\
        """)
        example_user_prompt_1 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedorder (
              order_id INTEGER PRIMARY KEY,
              account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
              amount REAL,
            );
            CREATE TABLE completedtrans (
              trans_id TEXT PRIMARY KEY,
              account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
              amount REAL,
              balance REAL,
            );
            CREATE TABLE completedacct (
              account_id TEXT PRIMARY KEY,
              frequency TEXT,
              parseddate TEXT,
            );
            CREATE TABLE completedclient (
              client_id TEXT PRIMARY KEY,
              name TEXT,
            );
            CREATE TABLE completeddisposition (
              disp_id TEXT PRIMARY KEY,
              client_id TEXT FOREIGN KEY REFERENCES completedclient(client_id),
              account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
            );
            
            The query to be answered is as follows: What are the names of my most valuable clients.\
        ''')
        example_assistant_response_1 = dedent('''\
            {
                "requirements": [
                    "names of each client"
                    "total number of orders per client",
                    "total number of transactions per client",
                    "total amount spent of orders per client",
                    "total amount spent on transactions per client"
                ],
                "axis": "client_id"
            }\
        ''')
        example_user_prompt_2 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedemployee (
              employee_id INTEGER PRIMARY KEY
              position TEXT CHECK( position IN ('data scientist, manager, CEO') ),
              salary INTEGER,
            );
            
            The query to be answered is as follows: What is the average salary of a data scientist\
        ''')
        example_assistant_response_2 = dedent('''\
            {
                "requirements": [
                    "average salary of data scientist"
                ],
                "axis": "position"
            }\
        ''')
        user_prompt = dedent(f'''\
            Here is the database schema:
            {self.database.getTextSchema()}
            
            The query to be answered is as follows: {query}.\
        ''')
        response = get_gpt_response(
            ("system", system_prompt),
            ("user", example_user_prompt_1),
            ("assistant", example_assistant_response_1),
            ("user", example_user_prompt_2),
            ("assistant", example_assistant_response_2),
            ("user", user_prompt),
            gpt4 = False,
            jsonMode = True
        )
        response_json = json.loads(response)
        return response_json

    def get_action(self, requirements: Dict[str, Union[List[str], str]])-> Dict[str, List[Dict[str, Any]]]:
        system_prompt = dedent('''\
            You are a data consultant, giving advice to the user. You will be provided with a list of datapoints which need to be extracted from a database. The database schema will be provided. Respond with details on how to extract each data.
            
            Respond with the following JSON object.
            {
                "action_infos": []
            }

            The "action_infos" field should contain a list of action_info objects, each one corresponding with one of the datapoints to be extracted. To create action_info objects, follow these steps:
            
            First, determine whether it's possible to extract the information from the database. If not, respond with the following JSON object. Note, only use this option as a last resort. The field 'message' should contain the reason why the data cannot be extracted
            
            {
                "status": "error",
                "error": "DATA_NOT_FOUND"
                "message": ""
            }
            
            If it's possible, respond with a JSON object of the following structure.
            
            {
                "status": "success",
                "command": "",
                "relevant_columns": [],
            }

            The 'command' field should contain actionable steps in an imperative mood to find the required information. Make sure that each table contains a relevant primary key for ease of joining in the future.
            
            The 'relevant_columns' field should contain a list of fields from the database which will be needed to generate SQL code to extract the data. Make sure each field is exactly as shown in the schema.

            Answer in a consistent style.\
        ''')
        example_user_prompt_1 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedorder (
              order_id INTEGER PRIMARY KEY,
              account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
              amount REAL,
            );
            CREATE TABLE completedtrans (
              trans_id TEXT PRIMARY KEY,
              account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
              amount REAL,
              balance REAL,
            );
            CREATE TABLE completedacct (
              account_id TEXT PRIMARY KEY,
              frequency TEXT,
              parseddate TEXT,
            );
            CREATE TABLE completedclient (
              client_id TEXT PRIMARY KEY,
              name TEXT,
            );
            CREATE TABLE completeddisposition (
              disp_id TEXT PRIMARY KEY,
              client_id TEXT FOREIGN KEY REFERENCES completedclient(client_id),
              account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
            );
            
            Provide details for extracting the following: names of each client, total number of orders per client.
            Please make sure for each datapoint, the resulting table contains the column: client_id. If the column cannot be directly included, find a way to include the column through a series of JOIN operations. This will be used the join the resulting tables together.\
        ''')
        example_assistant_response_1 = dedent('''\
            {
                "action_infos": [
                    {
                        "status": "success",
                        "command": "Join the completedclient, completeddisposition, and completedorder tables on their respective keys, then group by client_id and count the number of orders for each client.",
                        "relevant_columns": ["completedclient.client_id", "completeddisposition.client_id", "completeddisposition.account_id", "completedorder.account_id"]
                    },
                    {
                        "status": "success",
                        "command": "Join the completedclient, completeddisposition, and completedtrans tables on their respective keys, then group by client_id and sum the amount for each client.",
                        "relevant_columns": ["completedclient.client_id", "completeddisposition.client_id", "completeddisposition.account_id", "completedtrans.account_id", "completedtrans.amount"]
                    }
                ]
            }\
        ''')
        example_user_prompt_2 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedemployee (
              employee_id INTEGER PRIMARY KEY
              position TEXT CHECK( position IN ('data scientist, manager, CEO') ),
              salary INTEGER,
            );
            
            Provide details for extracting the following: average salary of analyst, average salary of data scientist.
            Please make sure for each datapoint, the resulting table contains a common column: position. If the column cannot be directly included, find a way to include the column through a series of JOIN operations. This will be used the join the resulting tables together.\
        ''')
        example_assistant_response_2 = dedent('''\
            {
                "action_infos": [
                    {
                        "status": "error",
                        "error": "DATA_NOT_FOUND"
                    },
                    {
                        "status": "success",
                        "command": "Average over the salary of each employee with a data scientist position. Include the employee position as a column.",
                        "relevant_columns": ["completedemployee.position", "completedemployee.salary"]
                    }
                ]
            }\
        ''')
        user_prompt = dedent(f'''\
            Here is the database schema:
            {self.database.getTextSchema()}
            
            Provide details for extracting the following: {', '.join(requirements['requirements'])}.
            Please make sure for each datapoint, the resulting table contains a common column: {requirements['axis']}. If the column cannot be directly included, find a way to include the column through a series of JOIN operations. This will be used the join the resulting tables together.\
        ''')
        response = get_gpt_response(
            ("system", system_prompt),
            ("user", example_user_prompt_1),
            ("assistant", example_assistant_response_1),
            ("user", example_user_prompt_2),
            ("assistant", example_assistant_response_2),
            ("user", user_prompt),
            gpt4 = True,
            jsonMode = True,
            top_p = 0.5
        )

        response_json = json.loads(response)
        return response_json['action_infos']
    
    def get_final_action(self, query: str) -> Dict[str, Union[str, List[str], Dict[str, str]]]:
        system_prompt = dedent('''\
            You are a data consultant, giving advice to the user. You will be provided with a question regarding some data in a database. All required information to answer the question should be in the database. The database schema will be provided. Respond with details on how to answer the question.
            
            Respond with a JSON object of the following structure.
            
            {
                "status": "success",
                "command": "",
                "relevant_columns": [],
                "graph_type": "",
                "graph_info": {}
            }

            The 'command' field should contain actionable steps in an imperative mood to find the required information. Assume if column names across tables are the same, they represent the same data and can be joined on.
            
            The 'relevant_columns' field should contain a list of columns from the dataframes which will be needed to generate SQL code to extract the data. Make sure each field is exactly as shown in the schema.

            The 'graph_type' field should contain a string of the name of the graph which should be used to best represent the required information.
            
            The 'graph_info' field should contain a JSON object providing details about the graph depending on which graph_type has been chosen.
            
            You may only choose from the following graph types and their corresponding graph_info:
            
        ''')
        for index, visualisation_class in enumerate(visualisation_subclasses.values()):
            system_prompt += dedent(f'''\
                {index+1}. {visualisation_class.getChartName()}
                {visualisation_class.getChartDescription()} The following values for graph_type and graph_info should be used. {visualisation_class.getChartParameterDescription()}
                    graph_type: '{visualisation_class.getChartName()}'
                    graph_info: {str(visualisation_class.getChartParametersForActioner())}

            ''')
        system_prompt += "Answer in a consistent style."
        example_user_prompt_1 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedorder (
              order_id INTEGER,
              account_id TEXT,
              amount REAL,
            );
            CREATE TABLE completedtrans (
              trans_id TEXT,
              account_id TEXT,
              amount REAL,
              balance REAL,
            );
            CREATE TABLE completedacct (
              account_id TEXT,
              frequency TEXT,
              parseddate TEXT,
            );
            CREATE TABLE completedclient (
              client_id TEXT,
              name TEXT,
            );
            CREATE TABLE completeddisposition (
              disp_id TEXT,
              client_id TEXT,
              account_id TEXT,
            );
            
            Provide details for extracting the following: total number of orders per client\
        ''')
        example_assistant_response_1 = dedent('''\
            {
                "status": "success",
                "command": "Join the completedclient, completeddisposition, and completedorder tables on their respective keys, then group by client_id and count the number of orders for each client",
                "relevant_columns": ["completedclient.name", "completedclient.client_id", "completeddisposition.client_id", "completeddisposition.account_id", "completedorder.account_id"]
                "graph_type": "Bar Chart"
                "graph_info": {
                    "title": 'Number of Orders per client',
                    "x_axis": 'client_id',
                    "y_axis": 'number_of_orders'
                },
            },\
        ''')
        example_user_prompt_2 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedemployee (
              employee_id INTEGER,
              position TEXT,
              salary INTEGER,
            );
            
            Provide details for extracting the following: average salary of data scientist\
        ''')
        example_assistant_response_2 = dedent('''\
            {
                "status": "success",
                "command": "Average over the salary of each employee with a data scientist position",
                "relevant_columns": ["completedemployee.position", "completedemployee.salary"],
                "graph_type": "No Chart"
                "graph_info": {},
            }
        ''')
        user_prompt = dedent(f'''\
            Here is the database schema:
            {self.database.getTextSchema()}

            Provide details for extracting the following: {query}
        ''')

        response = get_gpt_response(
            ("system", system_prompt),
            ("user", example_user_prompt_1),
            ("assistant", example_assistant_response_1),
            ("user", example_user_prompt_2),
            ("assistant", example_assistant_response_2),
            ("user", user_prompt),
            gpt4 = True,
            jsonMode = True,
            top_p = 0.5
        )
        response_json = json.loads(response)
        return response_json