import sqlvalidator
import sqlite3
from src.backend.utils.gpt import get_gpt_response
from src.backend.database import Database
from textwrap import dedent
from typing import List, Dict, Any, Union, Optional
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

    def __init__(self, database: Database, actionCommand: str, relevantColumns: List[str], graph_info: Optional[Dict[str, Union[str, Dict[str,str]]]] = None):
        self.database = database
        self.actionCommand = actionCommand
        self.graph_info = graph_info
        self.relevantColumns = relevantColumns
        self.is_single_value: bool = False

    def generateQuery(self) -> Dict[str, Union[str, Any]]:
        #method to generate SQL queries.
        system_prompt = dedent('''\
            As an SQL expert, your task is to generate SQL queries for users based on a provided database schema, an action command, relevant columns, and any specified graph information. Follow these steps to ensure accurate and effective SQL query generation:

            1. Analyze the given database schema, action command, relevant columns, and graph information.
            2. Determine if it is feasible to construct an SQL query that fulfills the action command:
            a. If the request cannot be fulfilled, return a JSON object with the status 'error' and an 'error' field specifying the reason. Use one of the predefined error values for clarity:
                {
                    "status": "error",
                    "error": "ERROR_DESCRIPTION"
                    "message": "ERROR_MESSAGE"
                }
                Replace "ERROR_DESCRIPTION" with:
                - "COLUMN_NOTIN_SCHEMA" if the relevant columns are not present in the database schema and the column cannot be recreated.
                - "INVALID_ACTION_COMMAND" if the action command cannot be executed due to logical reasons or missing information.
                - "GRAPH_INFO_NOT_APPLICABLE" if the graph information provided cannot be applied to the query due to schema constraints or relevancy issues.
                Replace "ERROR_MESSAGE" with a brief explanation of the error.
                For example:
                    when the action command is "Find the total number of customers who have made a purchase in the last 30 days", the relevant columns are "purchases.customer_id" and "purchases.purchase_date", and the graph information is "Pie Chart" with "customer_id" as the x-axis and "purchase_date" as the y-axis, the error should be "GRAPH_INFO_NOT_APPLICABLE" as a pie chart is not suitable for the given graph information.

            b. If the request can be fulfilled, construct and return a JSON object with the status 'success' and a 'query' field containing the SQL query. Make sure the SQL query is compatible with the DBMS SQLite3:
                {
                    "status": "success",
                    "query": \'\'\'SQL_QUERY_HERE\'\'\'
                    "is_single_value": "True/False"
                }
                Ensure "SQL_QUERY_HERE" accurately reflects the SQL command designed to address the action command, adhering to the database schema and incorporating the relevant columns and graph information as necessary. Make sure to only use columns given under relevant columns.
                
                For example:
                    when the action command is "Find the total number of customers who have made a purchase in the last 30 days", the relevant columns are "purchases.customer_id" and "purchases.purchase_date", and the graph information is "Bar Chart" with "customer_id" as the x-axis and "purchase_date" as the y-axis, the SQL query should be constructed to calculate the total number of customers who have made a purchase in the last 30 days and generate a bar chart based on the specified graph information. 
                    the JSON object should look like this:
                    {
                        "status": "success",
                        "query": \'\'\'SELECT COUNT(customer_id) FROM purchases WHERE purchase_date >= DATE('now', '-30 days')\'\'\'
                        "is_single_value": "True"
                    }                    

            Note: When constructing SQL queries, consider all provided information, ensure syntax correctness, and validate that the query logically aligns with the action command's requirements and the database schema's constraints.
            Note: make sure to use backslash to escape the necessary quotes in the query string.
            Note: please return only the JSON object with the status and the query field. Do not include any additional information in the response.\
        ''')
        user_prompt = dedent(f'''\
            Here is the database schema:
            {self.database.getTextSchema()}

            Here is the action command:
            {json.dumps(self.actionCommand)}

            Here are the relevant columns:
            {self.relevantColumns}

            Here is the graph information if any:
            {"None" if self.graph_info is None else self.graph_info}

            Generate an SQL query that fulfills the action command, incorporates the relevant columns, and applies the graph information as necessary.\
        ''')
        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", user_prompt),
            jsonMode = True,
            top_p = 0.2
        )
        gpt_response = json.loads(gpt_response)
        return gpt_response

    def parseQuery(self, gpt_response: Dict[str, Any]):
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
            self.is_single_value = gpt_response["is_single_value"]=="True"
            return query
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

        return gpt_response

    def validateQuery(self, query):
        #Validates the generated SQL query
        #returns None or raises Error
        sql_query = sqlvalidator.parse(query)
        if not sql_query.is_valid():
            raise QueryValidationError(f"SQL query is not valid: {sql_query.errors}")
        else:
            try:
                self.database.query(query,is_df=False,is_single_value=self.is_single_value)
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
    
    def getQuery(self):
        try:
            response = self.generateQuery()
            query = self.parseQuery(response)
            self.validateQuery(query)
            return query
        except Exception as e:
            print(e)
            return None
    
    def executeQuery(self, query):
        #Executes the SQL query and returns the results as a pandas DataFrame
        try:
            df = self.database.query(query, is_df=True, is_single_value=self.is_single_value)
            return df
        except Exception as e:
            print(e)
            return None