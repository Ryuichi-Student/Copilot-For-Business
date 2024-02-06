import pandas
from src.backend.utils.gpt import get_gpt_response
from src.backend.utils.database import Database
from textwrap import dedent
from typing import List, Dict, Any, Union
import json

class SQLGenerator:
    #Core class for generating SQL queries.

    def __init__(self, database: Database, actionCommand: str, graph_info: Dict[str, Union[str, Dict[str,str]]], relevantColumns: List[str]):
        self.database = database
        self.actionCommand = actionCommand
        self.graph_info = graph_info
        self.relevantColumns = relevantColumns

    def generateQuery(self) -> Dict[str, Union[str, Any]]:
        #method to generate SQL queries.
        system_prompt = """
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

           b. If the request can be fulfilled, construct and return a JSON object with the status 'success' and a 'query' field containing the SQL query:
              {
                  "status": "success",
                  "query": '''SQL_QUERY_HERE'''
              }
              Ensure "SQL_QUERY_HERE" accurately reflects the SQL command designed to address the action command, adhering to the database schema and incorporating the relevant columns and graph information as necessary.
              For example:
                when the action command is "Find the total number of customers who have made a purchase in the last 30 days", the relevant columns are "purchases.customer_id" and "purchases.purchase_date", and the graph information is "Bar Chart" with "customer_id" as the x-axis and "purchase_date" as the y-axis, the SQL query should be constructed to calculate the total number of customers who have made a purchase in the last 30 days and generate a bar chart based on the specified graph information. 
                the JSON object should look like this:
                {
                    "status": "success",
                    "query": '''SELECT COUNT(customer_id) FROM purchases WHERE purchase_date >= DATE('now', '-30 days')'''
                }                    

        Note: When constructing SQL queries, consider all provided information, ensure syntax correctness, and validate that the query logically aligns with the action command's requirements and the database schema's constraints.
        Note: make sure to use backslash to escape the necessary quotes in the query string.
        Note: please return only the JSON object with the status and the query field. Do not include any additional information in the response.
        """
        schema_str = self.database.getTextSchema()
        user_prompt = dedent(f"""\
        Here is the database schema:
        {schema_str}
        Here is the action command:
        {self.actionCommand}
        Here are the relevant columns:
        {self.relevantColumns}
        Here is the graph information:
        {self.graph_info}
        Generate an SQL query that fulfills the action command, incorporates the relevant columns, and applies the graph information as necessary.
        """)
        # print(user_prompt)
        gpt_response = get_gpt_response(
            ("system", system_prompt),
            ("user", user_prompt),
            jsonMode = True,
        )
        # query = self._parseQuery(gpt_response)
        gpt_response = json.loads(gpt_response)
        return gpt_response

    def _parseQuery(self, gpt_response):
        #extract Query from GPT response

        query = gpt_response.splitlines()[0]
        #dostuff
        return query

    def validateQuery(self, query):
        #Validates the generated SQL query
        #returns None or raises Error
        if not query.lower().startswith("select"):
            #raiseSomeError
            pass

    def executeQuery(self, query):
        #Executes the SQL query and returns the results as a pandas DataFrame
        try:
            df = self.database.query(query)
            return df
        except:
            #raiseSomeError
            pass