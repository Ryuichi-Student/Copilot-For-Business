import sqlvalidator
import sqlite3
import pandas as pd
from src.backend.utils.gpt import get_gpt_response
from src.backend.database import Database
from pprint import pprint
from src.backend.visualisation import visualisation_subclasses
from textwrap import dedent
from typing import List, Dict, Any, Union, Optional, Tuple
import json


class ResponseError(Exception):
    pass
class ResponseNotJSONError(ResponseError):
    pass

class ResponseContentMissingError(ResponseError):
    pass

class ResponseStatusError(ResponseError):
    pass

class Status_COLUMN_NOTIN_SCHEMA_Error(ResponseStatusError):
    pass

class Status_INVALID_ACTION_COMMAND_Error(ResponseStatusError):
    pass

class Status_GRAPH_INFO_NOT_APPLICABLE_Error(ResponseStatusError):
    pass

class InvalidQueryError(Exception):
    pass

class QueryValidationError(InvalidQueryError):
    pass

class QueryExecutionError(InvalidQueryError):
    pass

class SQLGenerator:
    #Core class for generating SQL queries.

    def __init__(self, database: Database, actionCommands: List[str], relevantColumns: List[List[str]], graph_infos: List[Optional[Dict[str, Union[str, Dict[str,str]]]]] = []):
        self.database = database
        self.actionCommands = actionCommands
        self.graph_infos = graph_infos
        self.relevantColumns = relevantColumns

    def generateQuery(self) -> Dict[str, List]:
        #method to generate SQL queries.
        system_prompt = dedent('''\
            As an SQL expert, your objective is to generate a list of SQL query objects tailored to user requests. These requests are based on a specified database schema, a set of action commands, relevant columns, and, when applicable, graph information that aligns with each action command.

        Your response should be formatted as a JSON object containing an array of SQL query objects, structured as follows:

        {
            "SQL_queries": []
        }

        Within this structure, each SQL query object corresponds to a specific action command, incorporating the relevant columns and any associated graph information. To ensure the generation of accurate and effective SQL query objects, please adhere to the following guidelines:

        1. Comprehend the Request: Examine the database schema, action command, relevant columns, and graph information provided for each SQL query object.

        2. Feasibility Check: Determine whether it's possible to construct an SQL query that meets the requirements of the action command. This process involves two scenarios:

        - Infeasibility: If constructing a corresponding SQL query is not possible, update the JSON object for the current SQL query object to indicate an error. This should include a status of 'error', an error field with a predefined error value, and a message providing a brief error explanation. Use the following template:

            {
                "status": "error",
                "error": "ERROR_DESCRIPTION",
                "message": "ERROR_MESSAGE"
            }

            Replace ERROR_DESCRIPTION with one of the following, as appropriate:
            - COLUMN_NOTIN_SCHEMA if the relevant columns are not in the database schema.
            - INVALID_ACTION_COMMAND if the action command is logically unexecutable.
            - GRAPH_INFO_NOT_APPLICABLE if the graph information does not suit the query context.

            And ERROR_MESSAGE with a concise explanation of the issue.

        - Feasibility: If the query can be constructed, the JSON object for the current SQL query object should reflect a status of 'success' and contain a query field with the SQL query. 
                Ensure compatibility with SQLite3 and use backslashes to escape quotes within the query string. 
                Include a is_single_value field to indicate if the query returns a single value ("True" or "False"). This should be "True" only when the query result is expected to produce a single row and a single column. 
                If the sql query will produce multiple columns, single value should be False!!!!
                For example:

            {
                "status": "success",
                "query": "SQL_QUERY_HERE",
                "is_single_value": "True/False"
            }

            Ensure the query aligns with the action command, adhering to the database schema and incorporating relevant columns and graph information as necessary. 
            Always select the primary key column in the generated query to facilitate future join operations.

        Key Considerations:

        - Focus on the provided information to construct each SQL query object, ensuring the syntax is correct and logically aligns with the action command's requirements and the database schema's constraints.
        - Use backslashes to escape quotes in the SQL query string.
        - Your response should strictly contain the JSON object with "SQL_queries" field and a list of SQL query object conforming to the specified format. Avoid including extraneous information.
        - Use the primary key and foreign key relationships to join the tables whenever necessary.
        \
        ''')
        
        actionCommandsDetails = []
        for i, actionCommand in enumerate(self.actionCommands):
            actionCommandStr = actionCommand
            relevantColumnsStr = str(self.relevantColumns[i])  # convert list to string
            graphInfoStr = "None" if self.graph_infos[i] is None else str(self.graph_infos[i])  # convert dict to string
            
            actionCommandsDetails.append(f'''
            Here is the action command {i + 1}:
            {actionCommandStr}

            Here are the relevant columns for action command {i + 1}:
            {relevantColumnsStr}

            Here is the graph information for action command {i + 1}, if any:
            {graphInfoStr}
            ''')

        actionCommandsDetailsStr = "\n".join(actionCommandsDetails)

        user_prompt = dedent(f'''
                    Here is the database schema:
                    {self.database.getTextSchema()}

                    {actionCommandsDetailsStr}

                    Generate SQL queries that fulfill each action command, incorporate the relevant columns, and apply the graph information as necessary.
                ''')

        example_user_prompt_1 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedorder (
                order_id INTEGER PRIMARY KEY,
                account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
                amount REAL
            );
            CREATE TABLE completedtrans (
                trans_id TEXT PRIMARY KEY,
                account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
                amount REAL,
                balance REAL
            );
            CREATE TABLE completedacct (
                account_id TEXT PRIMARY KEY,
                frequency TEXT,
                parseddate TEXT
            );
            CREATE TABLE completedclient (
                client_id TEXT PRIMARY KEY,
                name TEXT
            );
            CREATE TABLE completeddisposition (
                disp_id TEXT PRIMARY KEY,
                client_id TEXT FOREIGN KEY REFERENCES completedclient(client_id),
                account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id)
            );
            
            Here is the action command 1:
            Retrieve the total amount of orders for each client.

            Here are the relevant columns for action command 1:
            ["completedclient.name", "completedclient.client_id", "completedorder.account_id", "completedorder.amount"]

            Here is the graph information for action command 1, if any:
            {
                "graph_type": "Bar Chart", 
                "graph_info": {"title": "Total Order Amount per Client", "x_axis": "client_id", "y_axis": "total_amount"}
            }
            
            Here is the action command 2:
            Count the number of transactions per account.

            Here are the relevant columns for action command 2:
            ["completedacct.account_id", "completedtrans.account_id"]

            Here is the graph information for action command 2, if any:
            {
                "graph_type": "Pie Chart", 
                "graph_info": {"title": "Transactions per Account", "x_axis": "account_id", "y_axis": "transaction_count"}
            }
            \
        ''')

        example_assistant_response_1 = dedent('''\
            {
                "SQL_queries": [
                    {
                        "status": "success",
                        "query": "SELECT completedclient.name, completedclient.client_id, SUM(completedorder.amount) AS total_amount FROM completedclient JOIN completeddisposition ON completedclient.client_id = completeddisposition.client_id JOIN completedorder ON completeddisposition.account_id = completedorder.account_id GROUP BY completedclient.client_id",
                        "is_single_value": "False"
                    },
                    {
                        "status": "success",
                        "query": "SELECT completedacct.account_id, COUNT(completedtrans.trans_id) AS transaction_count FROM completedacct JOIN completedtrans ON completedacct.account_id = completedtrans.account_id GROUP BY completedacct.account_id",
                        "is_single_value": "False"
                    }
                ]
            }
        ''')

        example_user_prompt_2 = dedent('''\
            Here is the database schema:
            CREATE TABLE completedorder (
                order_id INTEGER PRIMARY KEY,
                account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
                amount REAL
            );
            CREATE TABLE completedtrans (
                trans_id TEXT PRIMARY KEY,
                account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
                amount REAL,
                balance REAL
            );
            CREATE TABLE completedacct (
                account_id TEXT PRIMARY KEY,
                frequency TEXT,
                parseddate TEXT
            );
            CREATE TABLE completedclient (
                client_id TEXT PRIMARY KEY,
                name TEXT
            );
            CREATE TABLE completeddisposition (
                disp_id TEXT PRIMARY KEY,
                client_id TEXT FOREIGN KEY REFERENCES completedclient(client_id),
                account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id)
            );
            
            Here is the action command 1:
            Find the total amount of loans for each client.

            Here are the relevant columns for action command 1:
            ["completedclient.name", "completedclient.client_id", "completedloan.account_id", "completedloan.payments"]
                            
            Here is the graph information for action command 1, if any:
            {
                "graph_type": "Bar Chart", 
                "graph_info": {"title": "Total Loan Amount per Client", "x_axis": "client_id", "y_axis": "total_amount"}
            }
            
            Here is the action command 2:
            Find the order id of the highest order amount.
                                       
            Here are the relevant columns for action command 2:
            ["completedorder.order_id", "completedorder.amount"]

            Here is the graph information for action command 2, if any:
            None
            \
        ''')

        example_assistant_response_2 = dedent('''\
            {
                "SQL_queries": [
                    {
                        "status": "error",
                        "error": "COLUMN_NOTIN_SCHEMA",
                        "message": "The completedloan.account_id and completedloan.payments columns are not in the database schema. Please provide valid columns."
                    },
                    {
                        "status": "success",
                        "query": "SELECT completedorder.order_id FROM completedorder WHERE completedorder.amount = (SELECT MAX(completedorder.amount) FROM completedorder)",
                        "is_single_value": "True"
                    }
                ]
            }
        ''')

        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", example_user_prompt_1),
            ("assistant", example_assistant_response_1),
            ("user", example_user_prompt_2),
            ("assistant", example_assistant_response_2),
            ("user", user_prompt),
            jsonMode = True,
            top_p = 0.2
        )
        gpt_response = json.loads(gpt_response)
        return gpt_response

    def parseQuery(self, gpt_response: Dict[str, Any]) -> Optional[Tuple[str,bool]]:
        #extract Query from GPT response
        if not isinstance(gpt_response, dict):
            raise ResponseNotJSONError(f"GPT response is not a JSON object, but a {type(gpt_response)}")
        if "status" not in gpt_response:
            raise ResponseContentMissingError(f"Status field is missing from GPT response")
        if gpt_response["status"] == "success":
            if "query" not in gpt_response:
                raise ResponseContentMissingError(f"Query field is missing from GPT response")
            query = gpt_response["query"]
            if "is_single_value" not in gpt_response:
                raise ResponseContentMissingError(f"is_single_value field is missing from GPT response")
            is_single_value = gpt_response["is_single_value"]=="True"
            pprint(query)
            return (query, is_single_value)
        elif gpt_response["status"] == "error":
            if "error" not in gpt_response:
                raise ResponseContentMissingError(f"Error field is missing from GPT response")
            if gpt_response["error"] == "COLUMN_NOTIN_SCHEMA":
                raise Status_COLUMN_NOTIN_SCHEMA_Error(f"Error: {gpt_response['message']}")
            elif gpt_response["error"] == "INVALID_ACTION_COMMAND":
                raise Status_INVALID_ACTION_COMMAND_Error(f"Error: {gpt_response['message']}")
            elif gpt_response["error"] == "GRAPH_INFO_NOT_APPLICABLE":
                raise Status_GRAPH_INFO_NOT_APPLICABLE_Error(f"Error: {gpt_response['message']}")
            else:
                raise ResponseStatusError(f"Error: {gpt_response['error']}")
        else:
            raise ResponseStatusError(f"Error: {gpt_response['error']}")
    

    def validateQuery(self, query: str, is_single_value: bool = False):
        #Validates the generated SQL query
        #returns None or raises Error
        sql_query = sqlvalidator.parse(query)
        if not sql_query.is_valid():
            raise QueryValidationError(f"SQL query is not valid: {sql_query.errors}")
        else:
            try:
                self.database.query(query, is_df=False, is_single_value=is_single_value)
            except sqlite3.OperationalError as e:
                raise QueryExecutionError(f"Sqlite3 Operational Error: {e}")
            except sqlite3.ProgrammingError as e:
                raise QueryExecutionError(f"Sqlite3 Programming Error: {e}")
            except sqlite3.IntegrityError as e:
                raise QueryExecutionError(f"Sqlite3 Integrity Error: {e}")
            except sqlite3.NotSupportedError as e:
                raise QueryExecutionError(f"Sqlite3 Not Supported Error: {e}")
            except sqlite3.DataError as e:
                raise QueryExecutionError(f"Sqlite3 Data Error: {e}")
            except sqlite3.InternalError as e:
                raise QueryExecutionError(f"Sqlite3 Internal Error: {e}")
            except sqlite3.DatabaseError as e:
                raise QueryExecutionError(f"Sqlite3 Database Error: {e}")
            except sqlite3.Error as e:
                raise QueryExecutionError(f"Sqlite3 Error: {e}")
    
    def getQueries(self)-> Tuple[List[Optional[str]], List[Optional[bool]]]:
        response = self.generateQuery()
        queries = []
        is_svs = []
        for query_obj in response["SQL_queries"]:
            try:
                query, is_single_value = self.parseQuery(query_obj) # type: ignore
                self.validateQuery(query, is_single_value)
                queries.append(query)
                is_svs.append(is_single_value)
            except Exception as e:
                pprint(f"{type(e).__name__}: {e}")
                queries.append(None)
                is_svs.append(None)
        return (queries, is_svs)

    
    def executeQuery(self, query: str, is_single_value = False) -> Optional[Union[pd.DataFrame, Any]]:
        #Executes the SQL query and returns the results as a pandas DataFrame
        try:
            df = self.database.query(query, is_df=True, is_single_value=is_single_value)
            return df
        except Exception as e:
            pprint(f"{type(e).__name__}: {e}")
            return None