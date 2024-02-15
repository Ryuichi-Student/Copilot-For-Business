import atexit
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import pandas as pd
from pprint import pprint

from src.backend.actioner import Actioner
from src.backend.database import SQLiteDatabase, DataFrameDatabase, Database
from src.backend.sql.generator import SQLGenerator
from src.backend.visualisation.PieChart import PieChart
from src.backend.visualisation import visualisation_subclasses


# TODO: After we finish everything, we can start making this into more than 2 layers.
# TODO: Parallelise actioncommands and sql query generation
class Query:
    def __init__(self, userQuery):
        self.userQuery = userQuery

        self.requirements = None
        self.actionCommands = None
        self.queries = None

        self.sql_generators = None
        self.answer = None
        self.plot = None
        self.dfs = None

    def set_requirements(self, actioner):
        print(self.requirements)
        if self.requirements is None:
            self.requirements = actioner.get_requirements(self.userQuery)

    def set_actionCommands(self, actioner):
        if self.actionCommands is None:
            if self.requirements is None:
                self.actionCommands = []
            else:
                self.actionCommands = [x for x in actioner.get_action(self.requirements) if x['status'] == 'success']
        print(f"ActionCommands: {self.actionCommands}")

    def create_sql_query(self, db, threadpool):

        if self.queries is None:
            if self.actionCommands is None or self.requirements is None:
                self.sql_generators = []
                self.queries = []
            else:
                self.sql_generators = [SQLGenerator(db, self.userQuery, actionCommand, self.requirements) for actionCommand in self.actionCommands]
                futures = [threadpool.submit(lambda: sql.getQuery()) for sql in self.sql_generators]
                self.queries = [future.result() for future in futures]

        print(f"Queries: {self.queries}")

    def execute_sql_queries(self, threadpool):
        if self.dfs is None:
            futures = [threadpool.submit(self.sql_generators[i].executeQuery, self.queries[i]) for i in range(len(self.queries))]
            self.dfs = [future.result() for future in futures]
        pprint(f"Dataframes: {self.dfs}")

    def get_plot(self, actioner: Actioner, database: Database):
        if self.plot is None and self.answer is None:
            cmd = actioner.get_final_action(self.userQuery)
            pprint(cmd)
            graph_info = cmd['graph_info']
            sql = SQLGenerator(database, cmd['command'], cmd['relevant_columns'], graph_info)
            query = sql.getQuery()
            pprint(query)
            df = sql.executeQuery(query)
            pprint(df)
            if isinstance(df, pd.DataFrame):
                vis = visualisation_subclasses[cmd['graph_type']](df, self.userQuery, graph_info)
                self.plot = vis.generate()
                pprint(self.plot)
            else:
                self.answer = df
        return self.plot

    def get_answer(self):
        return self.answer

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
            "dfs": self.dfs
        }


class Copilot:
    # TODO: Change this to use multiple databases.
    def __init__(self, db='databases/crm_refined.sqlite3', dbtype='sqlite', threadpool=ThreadPoolExecutor(max_workers=5)):
        if dbtype == "sqlite":
            self.db = SQLiteDatabase(db)
        self.UserQueries: Dict[int, Query] = {}
        self.actioner = Actioner(self.db)
        self.threadpool = threadpool
        atexit.register(self.cleanup)

    def query(self, _userQuery):
        userQuery = hash(_userQuery)
        if userQuery not in self.UserQueries:
            print("---------creating query--------")
            query = self.UserQueries[userQuery] = Query(_userQuery)
            print("---------setting requirements--------")
            query.set_requirements(self.actioner)
            print(query.requirements)
            print("---------setting actions--------")
            query.set_actionCommands(self.actioner)
            print("---------creating sql--------")
            query.create_sql_query(self.db, threadpool=self.threadpool)
            print("---------executing sql--------")
            query.execute_sql_queries(threadpool=self.threadpool)
            print(query.dfs)
            print("---------answering question--------")
            dfs_database = DataFrameDatabase(query.requirements, query.dfs)
            print("---------getting plot--------")
            plot = query.get_plot(Actioner(dfs_database), dfs_database)
            print(plot)

        return self.UserQueries[userQuery]

    def get_random_query(self):
        return self.UserQueries[list(self.UserQueries.keys())[0]]

    def get_requirements(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].requirements

    def get_actionCommands(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].actionCommands

    def get_sql(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].queries

    def get_dfs(self, query: str):
        return self.UserQueries[hash(query)].dfs

    def get_answer(self, query: str):
        return self.UserQueries[hash(query)].answer

    def get_plot(self, query: str):
        return self.UserQueries[hash(query)].plot

    def cleanup(self):
        print("Cleaning up threadpool")
        self.threadpool.shutdown(wait=False)
