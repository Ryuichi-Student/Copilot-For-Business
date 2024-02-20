import atexit
import time

import pandas as pd
from pprint import pprint
from typing import Dict
from concurrent.futures import ThreadPoolExecutor

from src.backend.actioner import Actioner
from src.backend.database import DataFrameDatabase, Database, SQLiteDatabase
from src.backend.sql.generator import SQLGenerator
from src.backend.visualisation import visualisation_subclasses

import streamlit as st


# TODO: After we finish everything, we can start making this into more than 2 layers.
class Query:
    def __init__(self, userQuery):
        self.userQuery = userQuery

        self.requirements = None
        self.actionInfos = None

        self.sql_generator = None
        self.queries = None
        self.dfs = None

        self.answer = None
        self.plot = None

    def set_requirements(self, actioner: Actioner):
        if self.requirements is None:
            self.requirements = actioner.get_requirements(self.userQuery)
            pprint(self.requirements)

    def set_actionInfos(self, actioner: Actioner):
        if self.actionInfos is None and self.requirements is not None:
            reqs = self.requirements
            actionInfos = actioner.get_action(reqs)
            self.actionInfos = {req:cmd for req,cmd in zip(reqs, actionInfos) if cmd['status'] == 'success'} # type: ignore
            pprint(self.actionInfos)

    def create_queries(self, db: Database, threadpool):
        if self.queries is None and self.actionInfos is not None:
            # self.sql_generators = {req:SQLGenerator(db, cmd['command'], cmd['relevant_columns']) for req,cmd in self.actionInfos.items()}
            action_commands, relevant_cols = [cmd['command'] for cmd in self.actionInfos.values()], [cmd["relevant_columns"] for cmd in self.actionInfos.values()]
            self.sql_generator = SQLGenerator(db, action_commands, relevant_cols, [None]*len(self.actionInfos))
            queries, _ = self.sql_generator.getQueries()
            # futures = {req:threadpool.submit(sql.getQuery) for req,sql in self.sql_generators.items()}
            # queries = {req:future.result() for req,future in zip(futures.keys(), futures.values())}
            # queries = {req:sql.getQuery() for req,sql in self.sql_generators.items()}
            self.queries = {req:query for req,query in zip(self.actionInfos.keys(), queries) if query is not None}
            pprint(self.queries)

    def get_dfs(self, threadpool):
        if self.dfs is None and self.sql_generator is not None and self.queries is not None:
            futures = {req:threadpool.submit(self.sql_generator.executeQuery, query) for req,query in self.queries.items()}
            dataframes = {req:future.result() for req,future in zip(futures.keys(), futures.values())}
            # dataframes = {req:self.sql_generators[req].executeQuery(query) for req,query in self.queries.items()}
            self.dfs = {req:df for req,df in dataframes.items() if df is not None and not df.empty}
            pprint(self.dfs)

    def get_plot(self, actioner: Actioner, database: Database):
        if self.plot is None and self.answer is None:
            cmd = actioner.get_final_action(self.userQuery)
            pprint(cmd)                
            graph_meta = {"graph_type": cmd["graph_type"], "graph_info": cmd['graph_info']}
            sql = SQLGenerator(database, [str(cmd['command'])], [cmd['relevant_columns']], [graph_meta]) # type: ignore
            queries, is_svs = sql.getQueries()
            query, is_sv = queries[0] if queries[0] is not None else "", is_svs[0] if is_svs[0] is not None else False
            pprint(query)
            df = sql.executeQuery(query, is_single_value=is_sv)
            pprint(df)
            if isinstance(df, pd.DataFrame):
                vis = visualisation_subclasses[str(cmd['graph_type'])](df, query, graph_meta["graph_info"])
                self.plot = vis.generate()
            else:
                self.answer = df

    def __dict__(self):
        """ JSON serialisable """
        return {
            "userQuery": self.userQuery,
            "requirements": self.requirements,
            "actionInfos": self.actionInfos,
            "sql_generator": self.sql_generator,
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
        self.status_placeholder = None
        atexit.register(self.cleanup)

    def query(self, _userQuery):
        if self.status_placeholder is None:
            raise Exception("status_placeholder is not set")
        userQuery = hash(_userQuery)
        if userQuery not in self.UserQueries:
            with self.status_placeholder:
                print("---------------------Creating a new query----------------------")
                st.write("Understanding the assignment")
                query = self.UserQueries[userQuery] = Query(_userQuery)

                print("---------------------Setting requirements----------------------")
                query.set_requirements(self.actioner)

                print("---------------------Setting actionInfos----------------------")
                st.write("Figuring out what to do")
                query.set_actionInfos(self.actioner)

                print("---------------------Creating queries----------------------")
                st.write("Creating subqueries")
                query.create_queries(self.db, threadpool=self.threadpool)

                print("---------------------Getting dataframes----------------------")
                st.write("Gathering required data")
                query.get_dfs(threadpool=self.threadpool)

                print("---------------------Getting plot----------------------")
                st.write("Getting an answer")
                dfs_database = DataFrameDatabase(self.get_dfs(_userQuery))
                query.get_plot(Actioner(dfs_database), dfs_database)

        return self.UserQueries[userQuery]

    def get_random_query(self):
        return self.UserQueries[list(self.UserQueries.keys())[0]]

    def get_requirements(self, query: str) -> list[str]:
        requirements = self.UserQueries[hash(query)].requirements
        if requirements is not None:
            return requirements
        raise Exception("unknown query")

    def get_actionInfos(self, query: str) -> list[str]:
        actionInfos = self.UserQueries[hash(query)].actionInfos
        if actionInfos is not None:
            return actionInfos
        raise Exception("unknown query")

    def get_sql(self, query: str) -> list[str]:
        queries = self.UserQueries[hash(query)].queries
        if queries is not None:
            return queries
        raise Exception("unknown query")

    def get_dfs(self, query: str) -> dict[str, pd.DataFrame]:
        dfs = self.UserQueries[hash(query)].dfs
        if dfs is not None:
            return dfs
        raise Exception("unknown query")

    def get_answer(self, query: str):
        return self.UserQueries[hash(query)].answer

    def get_plot(self, query: str):
        return self.UserQueries[hash(query)].plot

    def cleanup(self):
        print("Cleaning up threadpool")
        self.threadpool.shutdown(wait=False)

    def set_status_placeholder(self, animation_placeholder):
        self.status_placeholder = animation_placeholder
