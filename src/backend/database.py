from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Optional, Union, List, Dict, Any
import sqlite3
import pandas as pd
import pandasql as psql
import json
from src.backend.utils.gpt import *


class Database(ABC):
    def __init__(self, url: str, additionalMetadata: Optional[Dict[Any, Any]] = None):
        self._url: str = url
        self._schema: Dict[str, List[Dict[str, Union[str, bool, int]]]] = self.getSchema()
        self._tableNames: List[str] = self.getTableNames()
        self._columnNames: List[str] = self.getColumnNames()
        self._descriptionEmbeddings = self.getDescriptionEmbeddings()
        self.additionalMetadata: Dict[Any, Any] = additionalMetadata if additionalMetadata else {}

    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    @property
    def schema(self) -> Dict[str, List[Dict[str, Union[str, bool, int]]]]:
        return self._schema
    
    @property
    def tableNames(self) -> List[str]:
        return self._tableNames
    
    @property
    def columnNames(self) -> List[str]:
        return self._columnNames
    
    @property
    def descriptionEmbeddings(self) -> Dict[str, Dict[str, Union[str, List[float]]]]:
        return self._descriptionEmbeddings

    @abstractmethod
    def to_str(self) -> str:
        pass

    @abstractmethod
    def query(self, code: str, is_df: bool, is_single_value: bool) -> pd.DataFrame:
        pass

    @abstractmethod
    def getSchema(self) -> Dict[str, List[Dict[str, Union[str, bool, int]]]]:
        pass

    @abstractmethod
    def getTextSchema(self) -> str:
        pass

    @abstractmethod
    def getTableNames(self) -> List[str]:
        pass

    @abstractmethod
    def getColumnNames(self) -> List[str]:
        pass

    @abstractmethod
    def getDescriptionEmbeddings(self) -> Dict[str, Dict[str, Union[str, List[float]]]]:
        pass

class SQLiteDatabase(Database):
    def __init__(self, file_path, additionalMetadata=None):
        super().__init__(file_path, additionalMetadata)

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
                if not column['default_value'] == None:
                    text_schema += f' DEFAULT {column["default_value"]}'
                if column['is_primary']:
                    text_schema += f' PRIMARY KEY'
                if column['is_foreign']:
                    text_schema += f' FOREIGN KEY REFERENCES {column["is_foreign"]}'
                text_schema += ',\n'
            text_schema += ');\n'
        return text_schema

    def getTableNames(self) -> List[str]:
        with sqlite3.connect(self.url) as conn:
            return [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]

    def getColumnNames(self):
        with sqlite3.connect(self.url) as conn:
            # Assuming conn is your database connection and self.tableNames is a list of table names
            column_names = [column_name for tname in self.tableNames for column_name in [row[1] for row in conn.execute(f"PRAGMA table_info(\"{tname}\")")]]
            return column_names
    
    def getDescriptionEmbeddings(self, forceWrite=False):
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
            for table in self.tableNames:
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
        return table_description_embeddings

    def to_str(self):
        # Implement this method
        pass


class CSVDatabase(Database):
    def __init__(self, file_path, additionalMetadata=None):
        super().__init__(file_path, additionalMetadata)
        self.dataframe = pd.read_csv(self.url)

    def query(self, code, is_df, is_single_value):
        return psql.sqldf(code, locals())

    def getSchema(self):
        # Implement this method
        pass

    def getTextSchema(self):
        # Implement this method
        pass

    def getTableNames(self):
        # Implement this method
        pass

    def getColumnNames(self):
        # Implement this method
        pass

    def getDescriptionEmbeddings(self):
        # Implement this method
        pass