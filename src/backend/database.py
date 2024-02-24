from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Optional, Union, List, Dict, Any
import sqlite3
import pandas as pd
import pandasql as psql
import json
from src.backend.utils.clean_name import clean_name
from src.backend.utils.gpt import *


class Database(ABC):
    def __init__(self, additionalMetadata: Optional[Dict[Any, Any]] = None):
        self._schema: Dict[str, List[Dict[str, Union[str, bool, int]]]] = self.getSchema()
        self._tableNames: List[str] = self.getTableNames()
        self._columnNames: List[str] = self.getColumnNames()
        self.additionalMetadata: Dict[Any, Any] = additionalMetadata if additionalMetadata else {}

    @property
    def schema(self) -> Dict[str, List[Dict[str, Union[str, bool, int]]]]:
        return self._schema
    
    @property
    def tableNames(self) -> List[str]:
        return self._tableNames
    
    @property
    def columnNames(self) -> List[str]:
        return self._columnNames

    @abstractmethod
    def to_str(self) -> str:
        pass

    @abstractmethod
    def query(self, code: str, is_df: bool, is_single_value: bool) -> Optional[Union[Any, pd.DataFrame]]:
        pass

    @abstractmethod
    def getSchema(self) -> Dict[str, List[Dict[str, Union[str, bool, int]]]]:
        pass

    def getTextSchema(self, filterTableNames:Optional[List[str]] = None) -> str:
        # Turns schema into text. Assumes self._schema has been filled
        text_schema = ''
        schema = self.schema
        for table in schema:
            if filterTableNames is not None:
                if table not in filterTableNames:
                    continue
            text_schema += f'CREATE TABLE {table} (\n'
            for column in schema[table]:
                text_schema += f'  {column["column_name"]} {column["type"]}'
                if not column['nullable']:
                    text_schema += ' NOT NULL'
                if column['default_value'] is not None:
                    text_schema += f' DEFAULT {column["default_value"]}'
                if column['is_primary']:
                    text_schema += f' PRIMARY KEY'
                if column['is_foreign']:
                    text_schema += f' FOREIGN KEY REFERENCES {column["is_foreign"]}'
                text_schema += ',\n'
            text_schema += ');\n'
        return text_schema

    @abstractmethod
    def getTableNames(self) -> List[str]:
        pass

    @abstractmethod
    def getColumnNames(self) -> List[str]:
        pass

class SQLiteDatabase(Database):
    def __init__(self, file_path, additionalMetadata=None, progress_callback=None):
        self._url = file_path
        super().__init__(additionalMetadata)
        self._descriptionEmbeddings = self.getDescriptionEmbeddings(progress_callback=progress_callback)
    
    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, value: str) -> None:
        self._url = value
    
    @property
    def descriptionEmbeddings(self) -> Dict[str, Dict[str, Union[str, List[float]]]]:
        return self._descriptionEmbeddings

    def query(self, code, is_df = True, is_single_value = False):

        def check_single_value(cursor):
            first_result = cursor.fetchone()
            if first_result is not None:
                next_result = cursor.fetchone()
                return len(first_result) == 1 and next_result is None
            return False
        
        with sqlite3.connect("file:"+self.url+'?mode=ro', uri=True) as conn:
            if is_df:
                try:
                    df = pd.read_sql_query(code, conn)
                    if is_single_value and not df.shape == (1, 1):
                        raise RuntimeError("SQL query does not return single value, but single value expected")
                    if is_single_value:
                        return df.iloc[0, 0]
                    else:
                        return df
                except sqlite3.Error as e:
                    raise e
            else:
                cursor = conn.cursor()
                try:
                    cursor_result = cursor.execute(code)
                    if is_single_value and not check_single_value(cursor_result):
                        raise RuntimeError("SQL query does not return single value, but single value expected")
                except sqlite3.Error as e:
                    raise e
                except Exception as e:
                    raise e
                finally:
                    conn.rollback()

    def getSchema(self):
        # print(f"URL: {self.url}")
        with sqlite3.connect(self.url) as conn:
            # Get the list of tables
            tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            tables = [row[0] for row in conn.execute(tables_query)]
            schema : Dict[str, List[Dict[str, Union[str, bool, int]]]] = {}
            for table in tables:
                # Get the column details
                columns_query = f"PRAGMA table_info(\"{table}\")"
                columns = conn.execute(columns_query).fetchall()

                # Get foreign key details
                fk_query = f"PRAGMA foreign_key_list(\"{table}\")"
                fks = {fk[3]: (fk[2], fk[4]) for fk in conn.execute(fk_query)} # column_name: (foreign_table, foreign_column)

                schema[table] = []
                for col in columns:
                    column_name, col_type, nullable, default_value, pk = col[1:6]
                    column_info = {
                        "column_name": column_name,
                        "type": col_type,
                        "is_primary": pk != 0,
                        "is_foreign": f"{fks[column_name][0]}({fks[column_name][1]})" if column_name in fks else False,
                        "default_value": default_value,
                        "nullable": nullable == 0
                    }
                    schema[table].append(column_info)
            return schema
    
    def getTableNames(self) -> List[str]:
        with sqlite3.connect(self.url) as conn:
            return [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]

    def getColumnNames(self):
        with sqlite3.connect(self.url) as conn:
            # Assuming conn is your database connection and self.tableNames is a list of table names
            column_names = [column_name for tname in self.tableNames for column_name in [row[1] for row in conn.execute(f"PRAGMA table_info(\"{tname}\")")]]
            return column_names
    
    def getDescriptionEmbeddings(self, forceWrite=False, progress_callback=None):
        """
        Get the embedding of each table in the database. If forceWrite is true will overwrite the embedding file.
        """
        description_url = f'{self.url}.json'
        table_description_embeddings = {}
        try:
            if forceWrite:
                raise FileNotFoundError
            with open(description_url, 'r') as description_file:
                table_description_embeddings = json.load(description_file)
        except FileNotFoundError:
            if progress_callback is not None:
                progress_callback((0, len(self.tableNames)))
            for table in self.tableNames:
                if progress_callback is not None:
                    progress_callback(table)
                table_preview = self.query(f"SELECT * FROM \"{table}\" LIMIT 5").to_string(index=False)
                system_prompt = dedent("""\
                    You are a data consultant, giving descriptions to tables. You will be provided with a preview of the first 5 rows of a table. Please come up with a short, concise description in one or two sentences that gives an accurate overview of the table.\
                """)
                response = get_gpt_response(
                    ("system", system_prompt),
                    ("user", table_preview),
                    top_p = 0.5, frequency_penalty = 0, presence_penalty = 0
                )
                embedding = get_gpt_embedding(response)
                table_description_embeddings[table] = {
                    'description': response,
                    'embedding': embedding
                }

            with open(description_url, 'w') as description_file:
                json.dump(table_description_embeddings, description_file)

            print("=*==============================================")

            if progress_callback is not None:
                progress_callback((len(self.tableNames), len(self.tableNames)))
        return table_description_embeddings

    def to_str(self):
        # Implement this method
        pass


class DataFrameDatabase(Database):
    def __init__(self, dataframes: Dict[str, pd.DataFrame], additionalMetadata=None):
        self._dataframes = {clean_name(req):df for req,df in dataframes.items()}
        super().__init__(additionalMetadata)
    
    @property
    def dataframes(self) -> Dict[str, pd.DataFrame]:
        return self._dataframes

    def query(self, code, is_df = True, is_single_value = False):
        df = psql.sqldf(code, self.dataframes)
        if is_single_value and not df.shape == (1, 1):
            raise RuntimeError("SQL query does not return single value, but single value expected")
        if is_single_value:
            return df.iloc[0, 0]
        else:
            return df

    def getSchema(self):
        schema : Dict[str, List[Dict[str, Union[str, bool, int]]]] = {}
        for name, table in self.dataframes.items():
            schema[name] = []
            for col, col_type in zip(table.columns, table.dtypes):
                column_info = {
                    "column_name": col,
                    "type": col_type,
                    "is_primary": False,
                    "is_foreign": False,
                    "default_value": None,
                    "nullable": True
                }
                schema[name].append(column_info)
        return schema

    def getTableNames(self):
        return self.dataframes.keys()

    def getColumnNames(self):
        return [column for tname in self.tableNames for column in self.dataframes[tname].columns]

    def to_str(self):
        # Implement this method
        pass