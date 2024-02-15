import atexit
from concurrent.futures import as_completed, ThreadPoolExecutor

from src.backend.actioner import Actioner
from src.backend.database import SQLiteDatabase
from src.backend.sql.generator import SQLGenerator
from src.backend.visualisation.PieChart import PieChart


# TODO: After we finish everything, we can start making this into more than 2 layers.
# TODO: Parallelise actioncommands and sql query generation
class Query:
    def __init__(self, userQuery):
        self.userQuery = userQuery

        self.requirements = None
        self.actionCommands = None
        self.queries = None

        self.sql_generators = None
        self.answer = ""
        self.plot = None
        self.df = None

    def set_requirements(self, actioner):
        print(self.requirements)
        if self.requirements is None:
            self.requirements = actioner.get_requirements(self.userQuery)

    def set_actionCommands(self, actioner, threadpool):
        if self.actionCommands is None:
            if self.requirements is None:
                self.actionCommands = []
            else:
                futures = [threadpool.submit(actioner.get_action, req, self.userQuery) for req in self.requirements]
                self.actionCommands = [future.result() for future in futures]
        print(f"ActionCommands: {self.actionCommands}")

    def create_sql_query(self, db, threadpool):
        def _make_query(sql):
            q = sql.parseQuery(sql.generateQuery())
            if sql.validateQuery(q):
                return q
            else:
                print(f"Invalid SQL query: {q}")
                return q

        if self.queries is None:
            if self.actionCommands is None or self.requirements is None:
                self.sql_generators = []
                self.queries = []
            else:
                self.sql_generators = [SQLGenerator(db, self.userQuery, actionCommand, self.requirements) for actionCommand in self.actionCommands]
                futures = [threadpool.submit(lambda: _make_query(sql)) for sql in self.sql_generators]
                self.queries = [future.result() for future in futures]

        print(f"Queries: {self.queries}")

    def execute_sql_queries(self):
        if self.df is None:
            if self.queries is None:
                self.df = []
            else:
                self.df = [self.sql_generators[i].executeQuery(self.queries[i]) for i in range(len(self.queries))]
        print(f"Dataframes: {self.df}")

    def get_df(self):
        if self.df is None:
            # TODO: Ask GPT to now answer the question using the data that it now has.
            pass
        return self.df

    # TODO: Implement the methods below without hard coding
    def get_plot(self):
        # TODO: Use the get_df method to get the data instead of the following
        pie = PieChart("Customer value", self.df[0],
                       "SELECT c.first || ' ' || COALESCE(c.middle || ' ', '') || c.last AS Client_Name, SUM(t.amount) AS Total_Spending FROM completedtrans t JOIN completedacct a ON t.account_id = a.account_id JOIN completeddisposition d ON a.account_id = d.account_id JOIN completedclient c ON d.client_id = c.client_id GROUP BY c.client_id ORDER BY Total_Spending DESC",
                       "Client_Name", "Total_Spending")
        self.plot = {"df": self.df, "pie": pie}
        return self.plot

    def get_answer(self):
        return

    def __dict__(self):
        """ JSON serialisable """
        return {
            "userQuery": self.userQuery,
            "requirements": self.requirements,
            "actionCommands": self.actionCommands,
            "queries": self.queries,
            "sql_generators": self.sql_generators,
            "answer": self.answer,
            "plot": self.plot,
            "df": self.df
        }


class Copilot:
    # TODO: Change this to use multiple databases.
    def __init__(self, db='databases/crm_refined.sqlite3', dbtype='sqlite', threadpool=ThreadPoolExecutor(max_workers=5)):
        if dbtype == "sqlite":
            self.db = SQLiteDatabase(db)
        self.UserQueries = {}
        self.actioner = Actioner(self.db)
        self.threadpool = threadpool
        atexit.register(self.cleanup)

    def query(self, _userQuery):
        userQuery = hash(_userQuery)
        if userQuery not in self.UserQueries:
            query = self.UserQueries[userQuery] = Query(_userQuery)
            query.set_requirements(self.actioner)
            query.set_actionCommands(self.actioner, threadpool=self.threadpool)
            query.create_sql_query(self.db, threadpool=self.threadpool)
            query.execute_sql_queries()
            df = query.get_df()
            query.get_plot()

        return self.UserQueries[userQuery]

    def get_random_query(self):
        return self.UserQueries[list(self.UserQueries.keys())[0]]

    def get_requirements(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].requirements

    def get_actionCommands(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].actionCommands

    def get_sql(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].queries

    def get_df(self, query: str):
        return self.UserQueries[hash(query)].df

    def get_plot(self, query: str):
        return self.UserQueries[hash(query)].plot

    def cleanup(self):
        print("Cleaning up threadpool")
        self.threadpool.shutdown(wait=False)
