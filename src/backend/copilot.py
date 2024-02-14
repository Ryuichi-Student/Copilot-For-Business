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
        if self.requirements is None:
            self.requirements = actioner.get_requirements(self.userQuery)

    def set_actionCommands(self, actioner):
        if self.actionCommands is None:
            # Make this run in parallel
            self.actionCommands = [actioner.get_action(req, self.userQuery) for req in self.requirements]

    def create_sql_query(self, db):
        if self.queries is None:
            self.sql_generators = [SQLGenerator(db, self.userQuery, actionCommand, self.requirements) for actionCommand in self.actionCommands]
            # Make this run in parallel
            self.queries = [sql.validateQuery(sql.parseQuery(sql.generateQuery())) for sql in self.sql_generators]

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


class Copilot:
    # TODO: Change this to use multiple databases.
    def __init__(self, db='databases/crm_refined.sqlite3', dbtype='sqlite'):
        if dbtype == "sqlite":
            self.db = SQLiteDatabase(db)
        self.UserQueries = {}
        self.actioner = Actioner(self.db)

    def query(self, _userQuery):
        userQuery = hash(_userQuery)
        if userQuery not in self.UserQueries:
            query = self.UserQueries[userQuery] = Query(_userQuery)
            query.set_requirements(self.actioner)
            query.set_actionCommands(self.actioner)
            query.create_sql_query(self.db)
            df = query.get_df()
            query.get_plot()

        return self.UserQueries[userQuery]

    def get_requirements(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].requirements

    def get_actionCommands(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].actionCommands

    def get_sql(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].queries

    def get_df(self, query: str):
        return self.UserQueries[hash(query)].df
