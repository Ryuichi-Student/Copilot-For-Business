from abc import ABC, abstractmethod
from typing import Optional, Union, List, Dict, Any
import sqlite3
import pandas as pd
import pandasql as psql
from src.backend.utils.gpt import get_gpt_response


class Database(ABC):
    def __init__(self, url: str, additionalMetadata: Optional[Dict[Any, Any]] = None):
        self._url: str = url
        self._schema: Dict[str, Dict[str, Dict[str, Union[str, bool, int]]]] = self.getSchema()
        self._tableNames: List[str] = self.getTableNames()
        self._columnNames: List[str] = self.getColumnNames()
        self.additionalMetadata: Dict[Any, Any] = additionalMetadata if additionalMetadata else {}
        self._description: List[str] = self.getDescriptions()


    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, value: str) -> None:
        self._url = value
        
    @property
    def schema(self) -> Dict[str, Dict[str, Dict[str, Union[str, bool, int]]]]:
        return self._schema
    
    @property
    def description(self) -> List[str]:
        return self._description
    
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
    def query(self, code: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def getSchema(self) -> Dict[str, Dict[str, Dict[str, Union[str, bool, int]]]]:
        pass

    @abstractmethod
    def getDescriptions(self) -> List[str]:
        pass

    @abstractmethod
    def getTableNames(self) -> List[str]:
        pass

    @abstractmethod
    def getColumnNames(self) -> List[str]:
        pass

class SQLiteDatabase(Database):
    def __init__(self, file_path, additionalMetadata=None):
        super().__init__(file_path, additionalMetadata)

    def query(self, code):
        with sqlite3.connect(self.url) as conn:
            return pd.read_sql_query(code, conn)

    def getDescriptions(self)-> str:
        """
        Get the description of the database
        return: str
        """
        descriptions = []
        for table in self.tableNames:
            description = self.query(f"SELECT * FROM \"{table}\" LIMIT 1").to_string(index=False)
            descriptions.append(table)
            descriptions.append(description)
        table_descriptions = "\n".join(descriptions)
        question = f"Given this database schema: {self.schema}, as well as the following table descriptions: {table_descriptions}, come up with a structured, detailed description of the database."
        return get_gpt_response(("system", "You are a helpful assistant"), ("user", question))

    def getSchema(self):
        with sqlite3.connect(self.url) as conn:
            # Get the list of tables
            tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            tables = [row[0] for row in conn.execute(tables_query)]
            schema = {}
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

        

    def to_str(self):
        # Implement this method
        pass


class CSVDatabase(Database):
    def __init__(self, file_path, additionalMetadata=None):
        super().__init__(file_path, additionalMetadata)
        self.dataframe = pd.read_csv(self.url)

    def query(self, code):
        return psql.sqldf(code, locals())

    def getDescriptions(self):
        # Implement this method
        pass

    def getSchema(self):
        # Implement this method
        pass

    def getTableNames(self):
        # Implement this method
        pass

    def getColumnNames(self):
        # Implement this method
        pass

