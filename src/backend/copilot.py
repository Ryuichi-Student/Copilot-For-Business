import atexit
import time
import uuid

import pandas as pd
from pprint import pprint
from typing import Dict, List, Union
from concurrent.futures import ThreadPoolExecutor

from src.backend.actioner import Actioner
from src.backend.database import DataFrameDatabase, Database, SQLiteDatabase
from src.backend.sql.generator import SQLGenerator
from src.backend.visualisation import visualisation_subclasses
from src.backend.generalised_answer import general_answer_gen
from src.backend.utils.clean_name import clean_name
from src.backend.utils.early_analysis import early_analysis

import streamlit as st
import hashlib

# TODO: After we finish everything, we can start making this into more than 2 layers.
class Query:
    def __init__(self, userQuery):
        self.userQuery = userQuery

        self.requirements = None
        self.actionInfos = None

        self.sql_generator = None
        self.queries = None
        self.dfs = None

        self.early_answer = None
        self.answer = None
        self.plot = None
        self.generalised_answer = None
        self.final_action = None
        self.final_query = None
        self.final_df = None

    def early_analysis(self, db: Database)-> bool:
        response = early_analysis(self.userQuery, db)
        # pprint(response)
        if response["status"] == "schema":
            self.early_answer = response["message"]
            return True
        else:
            return False

    def set_requirements(self, actioner: Actioner):
        if self.requirements is None:
            self.requirements = actioner.get_requirements(self.userQuery)
            # pprint(self.requirements)

    def set_actionInfos(self, actioner: Actioner):
        if self.actionInfos is None and self.requirements is not None:
            reqs = self.requirements
            actionInfos = actioner.get_action(reqs)
            self.actionInfos = {req:cmd for req,cmd in zip(reqs['requirements'], actionInfos) if cmd['status'] == 'success'} # type: ignore
            # pprint(self.actionInfos)

    def create_queries(self, db: Database):
        if self.queries is None and self.actionInfos is not None and self.requirements is not None:
            action_commands, relevant_cols, primary_keys = [cmd['command'] for cmd in self.actionInfos.values()], [cmd["relevant_columns"] for cmd in self.actionInfos.values()], [self.requirements['axis']]*len(self.actionInfos)
            self.sql_generator = SQLGenerator(db, action_commands, relevant_cols, primary_keys, [None]*len(self.actionInfos))
            queries = self.sql_generator.getQueries()
            self.queries = {req:query for req,query in zip(self.actionInfos.keys(), queries) if query is not None}
            # pprint(self.queries)

    def get_dfs(self, threadpool):
        if self.dfs is None and self.sql_generator is not None and self.queries is not None:
            futures = {req:threadpool.submit(self.sql_generator.executeQuery, query) for req,query in self.queries.items()}
            dataframes = {req:future.result() for req,future in zip(futures.keys(), futures.values())}
            # dataframes = {req:self.sql_generators[req].executeQuery(query) for req,query in self.queries.items()}
            self.dfs = {}
            for req, df in dataframes.items():
                if isinstance(df, pd.DataFrame):
                    if df is not None and not df.empty:
                        self.dfs[req] = df
                else:
                    newdf = pd.DataFrame({clean_name(req): [df]})
                    self.dfs[req] = newdf
            # self.dfs = {req:df for req,df in dataframes.items() if df is not None and not df.empty}
            # pprint(self.dfs)

    def get_plot(self, actioner: Actioner, database: Database):
        if self.plot is None and self.answer is None and self.requirements is not None and self.queries is not None:
            cmd = actioner.get_final_action(self.userQuery)
            self.final_action = cmd
            # pprint(cmd)
            if "graph_type" not in cmd:
                self.plot = None
                return
            graph_meta = {"graph_type": cmd["graph_type"], "graph_info": cmd['graph_info']}
            sql = SQLGenerator(database, [str(cmd['command'])], [cmd['relevant_columns']], [self.requirements['axis']], [graph_meta])
            queries = sql.getQueries()
            query = queries[0] if queries[0] is not None else ""
            self.final_query = query
            # pprint(query)
            self.queries["Combine Subtables"] = query
            df = sql.executeQuery(query)
            self.final_df = df
            # pprint(df)
            if isinstance(df, pd.DataFrame) and cmd['graph_type']!="No Chart":
                vis = visualisation_subclasses[str(cmd['graph_type'])](df, query, graph_meta["graph_info"])
                self.plot = vis
            else:
                self.answer = df
    
    def get_generalised_answer(self):
        if self.generalised_answer is None:
            if self.plot is not None:
                answer_gen = general_answer_gen(str(self.plot),self.userQuery, self.final_action, [cmd['command'] for cmd in self.actionInfos.values()], True) # type: ignore
                self.generalised_answer = answer_gen.getAnswer()
            elif self.answer is not None:
                answer_gen = general_answer_gen(str(self.answer),self.userQuery, self.final_action, [cmd['command'] for cmd in self.actionInfos.values()], False) # type: ignore
                self.generalised_answer = answer_gen.getAnswer()
            else:
                self.generalised_answer = None

    def __dict__(self):
        """ JSON serialisable """
        return self.__getstate__()

    def __getstate__(self):
        return {
            "userQuery": self.userQuery,
            "requirements": self.requirements,
            "actionInfos": self.actionInfos,
            "early_answer": self.early_answer,
            "sql_generator": self.sql_generator,
            "queries": self.queries,
            "dfs": self.dfs,
            "answer": self.answer,
            "plot": self.plot,
            "generalised_answer": self.generalised_answer,
            "final_action": self.final_action,
            "final_query": self.final_query,
            "final_df": self.final_df
        }

    def __setstate__(self, state):
        self.userQuery = state["userQuery"]
        self.requirements = state["requirements"]
        self.actionInfos = state["actionInfos"]
        self.early_answer = state["early_answer"]
        self.sql_generator = state["sql_generator"]
        self.queries = state["queries"]
        self.dfs = state["dfs"]
        self.answer = state["answer"]
        self.plot = state["plot"]
        self.generalised_answer = state["generalised_answer"]
        self.final_action = state["final_action"]
        self.final_query = state["final_query"]
        self.final_df = state["final_df"]
        # print(self.early_answer)

class Copilot:
    # TODO: Change this to use multiple databases.
    def __init__(self, db='databases/crm_refined.sqlite3', dbtype='sqlite', threadpool=ThreadPoolExecutor(max_workers=5), potential_embedded=[], non_embedded=[]):
        
        if db is None:
            raise Exception("No database provided")
        else:
            print(f"Using database: {db}")

        if dbtype == "sqlite":
            self.db = SQLiteDatabase(db, potential_embedded=potential_embedded, non_embedded=non_embedded)
        self.UserQueries: Dict[str, Query] = {}
        self.actioner = Actioner(self.db)
        self.threadpool = threadpool
        self.status_placeholder = None
        atexit.register(self.cleanup)

    def query(self, _userQuery):
        if self.status_placeholder is None:
            raise Exception("status_placeholder is not set")
        # Maybe hash the query
        userQuery = _userQuery
        if userQuery not in self.UserQueries:
            with self.status_placeholder:
                print("---------------------Creating a new query----------------------")
                st.write("Understanding query")
                query = self.UserQueries[userQuery] = Query(_userQuery)

                print("---------------------Early Analysis----------------------")
                if query.early_analysis(self.db): # If the query can be answered by the schema
                    return self.UserQueries[userQuery]

                print("---------------------Setting requirements----------------------")
                query.set_requirements(self.actioner)

                print("---------------------Setting actionInfos----------------------")
                st.write("Creating subqueries")
                query.set_actionInfos(self.actioner)

                print("---------------------Creating queries----------------------")
                st.write("Processing subqueries")
                query.create_queries(self.db)

                print("---------------------Getting dataframes----------------------")
                st.write("Gathering required data")
                query.get_dfs(threadpool=self.threadpool)

                print("---------------------Getting plot----------------------")
                st.write("Generating answer")
                dfs_database = DataFrameDatabase(self.get_dfs(_userQuery))
                query.get_plot(Actioner(dfs_database), dfs_database)
                print("---------------------Getting generalised answer----------------------")
                query.get_generalised_answer()

        return self.UserQueries[userQuery]

    def get_random_query(self):
        return self.UserQueries[list(self.UserQueries.keys())[0]]

    def get_requirements(self, query: str) -> Dict[str, Union[List[str], str]]:
        requirements = self.UserQueries[query].requirements
        if requirements is not None:
            return requirements
        raise Exception("unknown query")

    def get_actionInfos(self, query: str) -> list[str]:
        actionInfos = self.UserQueries[query].actionInfos
        if actionInfos is not None:
            return actionInfos
        raise Exception("unknown query")

    def get_sql(self, query: str) -> list[str]:
        queries = self.UserQueries[query].queries
        if queries is not None:
            return queries
        raise Exception("unknown query")

    def get_dfs(self, query: str) -> dict[str, pd.DataFrame]:
        dfs = self.UserQueries[query].dfs
        if dfs is not None:
            return dfs
        raise Exception("unknown query")
    
    def get_final_df(self, query: str) -> pd.DataFrame:
        return self.UserQueries[query].final_df

    def get_early_answer(self, query: str):
        return self.UserQueries[query].early_answer

    def get_plot(self, query: str):
        return self.UserQueries[query].plot

    def get_generalised_answer(self, query: str):
        return self.UserQueries[query].generalised_answer

    def cleanup(self):
        print("Cleaning up threadpool")
        if hasattr(self, 'threadpool'):
            self.threadpool.shutdown(wait=False)

    def set_status_placeholder(self, animation_placeholder):
        self.status_placeholder = animation_placeholder

    def __getstate__(self):
        state = self.__dict__
        if 'threadpool' in state:
            self.threadpool.shutdown(wait=False)
            del state['threadpool']
        if 'status_placeholder' in state:
            del state['status_placeholder']
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        print(state)
        self.threadpool = ThreadPoolExecutor(max_workers=5)
        self.status_placeholder = None
        atexit.register(self.cleanup)