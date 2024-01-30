import sqlite3
import pandas as pd
import pandasql as psql

class Database:
    def __init__(self, url, additionalMetadata=None):
        self.url = url
        self.schema = self.getSchema()
        self.description = self.getDescriptions()
        self.additionalMetadata = additionalMetadata if additionalMetadata else {}

    def to_str(self):
        pass
        
    def query(self, code):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def getSchema(self):
        return {}

    def getDescriptions(self):
        return {}

class SQLiteDatabase(Database):
    def __init__(self, file_path, additionalMetadata=None):
        super().__init__(file_path, additionalMetadata)

    def query(self, code):
        with sqlite3.connect(self.url) as conn:
            return pd.read_sql_query(code, conn)
        
    def getDescriptions(self):
        raise NotImplementedError()
    
    def getSchema(self):
        raise NotImplementedError()
        

class CSVDatabase(Database):
    def __init__(self, file_path, additionalMetadata=None):
        super().__init__(file_path, additionalMetadata)
        self.dataframe = pd.read_csv(self.url)

    def query(self, code):
        return psql.sqldf(code, locals())
    
    def getDescriptions(self):
        raise NotImplementedError()
    
    def getSchema(self):
        raise NotImplementedError()