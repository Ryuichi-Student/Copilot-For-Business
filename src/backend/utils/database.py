from abc import ABC, abstractmethod
from typing import Optional, Union, List, Dict, Any
import sqlite3
import pandas as pd
import pandasql as psql

class Database(ABC):
    def __init__(self, url: str, additionalMetadata: Optional[Dict[Any, Any]] = None):
        self._url: str = url
        self._schema: Dict[str, Dict[str, Dict[str, Union[str, bool, int]]]] = self.getSchema()
        self._description: List[str] = self.getDescriptions()
        self._tableNames: List[str] = self.getTableNames()
        self._columnNames: List[str] = self.getColumnNames()
        self.additionalMetadata: Dict[Any, Any] = additionalMetadata if additionalMetadata else {}

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

