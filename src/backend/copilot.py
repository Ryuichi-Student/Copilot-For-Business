import atexit
import pandas as pd
from pprint import pprint
from typing import Dict
from concurrent.futures import as_completed, ThreadPoolExecutor

from src.backend.actioner import Actioner
from src.backend.database import DataFrameDatabase, Database, SQLiteDatabase
from src.backend.sql.generator import SQLGenerator
from src.backend.visualisation import visualisation_subclasses


# TODO: After we finish everything, we can start making this into more than 2 layers.
# TODO: Parallelise actionInfos and sql query generation
class Query:
    def __init__(self, userQuery):
        self.userQuery = userQuery

        self.requirements = None
        self.actionInfos = None

        self.sql_generators = None
        self.queries = None
        self.dfs = None

        self.answer = None
        self.plot = None

    def set_requirements(self, actioner: Actioner):
        if self.requirements is None:
            self.requirements = actioner.get_requirements(self.userQuery)
            pprint(self.requirements)

    def set_actionInfos(self, actioner: Actioner):
        if self.actionInfos is None:
            reqs = self.requirements
            actionInfos = actioner.get_action(reqs)
            self.actionInfos = {req:cmd for req,cmd in zip(reqs, actionInfos) if cmd['status'] == 'success'}
            pprint(self.actionInfos)

    def create_queries(self, db: Database, threadpool):
        # TODO: Add concurrency. as_completed does not maintain the input order. Is there some way to maintain it?
        if self.queries is None:
            self.sql_generators = {req:SQLGenerator(db, cmd['command'], cmd['relevant_columns']) for req,cmd in self.actionInfos.items()}
            # futures = {req:threadpool.submit(sql.getQuery) for req,sql in self.sql_generators.items()}
            # queries = {req:future.result() for req,future in zip(futures.keys(), as_completed(futures.values()))}
            queries = {req:sql.getQuery() for req,sql in self.sql_generators.items()}
            self.queries = {req:query for req,query in queries.items() if query is not None}
            pprint(self.queries)

    def get_dfs(self, threadpool):
        if self.dfs is None:
            # futures = {req:threadpool.submit(self.sql_generators[req].executeQuery, query) for req,query in self.queries.items()}
            # dataframes = {req:future.result() for req,future in zip(futures.keys(), as_completed(futures.values()))}
            dataframes = {req:self.sql_generators[req].executeQuery(query) for req,query in self.queries.items()}
            self.dfs = {req:df for req,df in dataframes.items() if df is not None and not df.empty}
            pprint(self.dfs)

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
            else:
                self.answer = df


    def __dict__(self):
        """ JSON serialisable """
        return {
            "userQuery": self.userQuery,
            "requirements": self.requirements,
            "actionInfos": self.actionInfos,
            "sql_generators": self.sql_generators,
            "queries": self.queries,
            "dfs": self.dfs,
            "answer": self.answer,
            "plot": self.plot,
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
            query = self.UserQueries[userQuery] = Query(_userQuery)
            query.set_requirements(self.actioner)
            query.set_actionInfos(self.actioner)
            query.create_queries(self.db, threadpool=self.threadpool)
            query.get_dfs(threadpool=self.threadpool)
            dfs_database = DataFrameDatabase(query.dfs)
            query.get_plot(Actioner(dfs_database), dfs_database)

        return self.UserQueries[userQuery]

    def get_random_query(self):
        return self.UserQueries[list(self.UserQueries.keys())[0]]

    def get_requirements(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].requirements

    def get_actionInfos(self, query: str) -> list[str]:
        return self.UserQueries[hash(query)].actionInfos

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
