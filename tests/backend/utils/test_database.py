from src.backend.utils.database import SQLiteDatabase
import sqlite3 as sql
import os
class TestSQLiteDatabase:

    def test_getSchema(self):
        # convert the relative file databases/crm1.db path to python os path
        relative_path = "databases/crm1"
        db = SQLiteDatabase(relative_path)
        schema = db.getSchema()
        print(schema)
        assert isinstance(schema, dict)
        assert len(schema) == 12
        assert isinstance(schema["completedorder"], list)
        assert len(schema["completedorder"]) == 6
        assert isinstance(schema["completedorder"][0], dict)
        assert len(schema["completedorder"][0]) == 6
        assert isinstance(schema["completedorder"][0]["column_name"], str)
        assert isinstance(schema["completedorder"][0]["type"], str)
        assert isinstance(schema["completedorder"][0]["nullable"], bool)
        assert isinstance(schema["completedorder"][0]["default_value"], (None.__class__, str))
        assert isinstance(schema["completedorder"][0]["is_primary"], bool)
        assert isinstance(schema["completedorder"][0]["is_foreign"], (bool, str))
        print(db.description)

    def testDBconnection(self):
        # convert the relative file databases/crm1.db path to python os path
        relative_path = "databases/crm1.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        sql.connect(absolute_path)

    def test_query(self):
        with sql.connect("Sample") as conn:
            tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            a = conn.execute(tables_query).fetchall()
            print(a)
        
