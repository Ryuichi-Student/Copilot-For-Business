import pandas

#we need to decide the structure of error-handling in our project

class SQLGenerator:
    #Core class for generating SQL queries.

    def __init__(self, database, actionCommand_obj, graph_info, relevantColumns):
        self.database = database
        self.actionCommand_obj = actionCommand_obj
        self.graph_info = graph_info
        self.relevantColumns = relevantColumns

    def generateQuery(self):
        #Abstract method to generate SQL queries.
        raise NotImplementedError("Abstract Method")
        """
        prompt = "Generate an SQL query based on the following action command: {self.actionCommand_obj}, considering {relevantColumns} and {graph_info}"
        gpt_response = get_gpt_response(prompt)
        query = self._parseQuery(gpt_response)
        self.validateQuery(query)
        return query
        """

    def _parseQuery(self, gpt_response):
        #extract Query from GPT response

        query = gpt_response.splitlines()[0]
        #dostuff
        return query

    def validateQuery(self, query):
        #Validates the generated SQL query
        #returns None or raises Error
        if not query.lower().startswith("select"):
            pass
            #raiseError

    def executeQuery(self, query):
        #Executes the SQL query and returns the results as a pandas DataFrame
        try:
            df = self.database.query(query)
            return df
        except:
            #raiseError
            pass