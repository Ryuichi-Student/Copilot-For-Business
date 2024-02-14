import atexit
from concurrent.futures import as_completed, ThreadPoolExecutor

from src.backend.actioner import Actioner
from src.backend.database import SQLiteDatabase
from src.backend.sql.generator import SQLGenerator


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
            futures = [threadpool.submit(actioner.get_action, req, self.userQuery) for req in self.requirements]
            self.actionCommands = [future.result() for future in as_completed(futures)]

    def create_sql_query(self, db, threadpool):
        if self.queries is None:
            self.sql_generators = [SQLGenerator(db, self.userQuery, actionCommand, self.requirements) for actionCommand in self.actionCommands]
            futures = [threadpool.submit(sql.validateQuery, sql.parseQuery(sql.generateQuery())) for sql in self.sql_generators]
            self.queries = [future.result() for future in as_completed(futures)]

    def get_df(self):
        if self.df is None:
            # TODO: Ask GPT to now answer the question using the data that it now has.
            pass
        return self.df

    # TODO: Implement these final two methods
    def get_plot(self):
        return

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

    def cleanup(self):
        print("Cleaning up threadpool")
        self.threadpool.shutdown(wait=False)
