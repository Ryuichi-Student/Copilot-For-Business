import sqlite3
import sys
import os
import pytest
import pandas as pd
from textwrap import dedent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.utils.database import SQLiteDatabase
import sqlite3 as sql


class TestSQLiteDatabase:

    def test_getSchema(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        # print(f"VERSION: {sqlite3.version}")
        db = SQLiteDatabase(absolute_path)
        schema = db.getSchema()
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
    
    def test_textSchema(self):
        db = SQLiteDatabase('databases/crm_refined.sqlite3')
        schema = db.getTextSchema(['completedorder'])
        assert schema == dedent('''\
        CREATE TABLE completedorder (
          order_id INTEGER PRIMARY KEY,
          account_id TEXT FOREIGN KEY REFERENCES completedacct(account_id),
          bank_to TEXT,
          account_to INTEGER,
          amount REAL,
          k_symbol TEXT,
        );
        ''')

    def test_DBconnection(self):
        # convert the relative file databases/crm1.db path to python os path
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        sql.connect(absolute_path)

    def test_query(self):
        with sql.connect("databases/crm_refined.sqlite3") as conn:
            tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            a = conn.execute(tables_query).fetchall()
            print(a)

    def test_modify_db(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        with pytest.raises(pd.errors.DatabaseError):
            db.query("DROP TABLE completedorder")
        with pytest.raises(pd.errors.DatabaseError):
            db.query("CREATE TABLE completedorder (order_id INTEGER PRIMARY KEY, account_id TEXT, bank_to TEXT, account_to INTEGER, amount REAL, k_symbol TEXT)")
        with pytest.raises(pd.errors.DatabaseError):
            db.query("INSERT INTO completedorder VALUES (1, '123', 'bank', 123, 123.0, 'symbol')")
        with pytest.raises(sql.OperationalError):
            db.query("DROP TABLE completedorder", is_df=False)
        with pytest.raises(sql.OperationalError):
            db.query("CREATE TABLE completedorder (order_id INTEGER PRIMARY KEY, account_id TEXT, bank_to TEXT, account_to INTEGER, amount REAL, k_symbol TEXT)", is_df=False)
        with pytest.raises(sql.OperationalError):
            db.query("INSERT INTO completedorder VALUES (1, '123', 'bank', 123, 123.0, 'symbol')", is_df=False)
    
    def test_singlevalue(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        response = db.query("SELECT COUNT(*) FROM completedorder", is_df=True, is_single_value=True)
        assert not isinstance(response, pd.DataFrame)

    def test_not_singlevalue(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        with pytest.raises(RuntimeError) as e:
            db.query("SELECT * FROM completedorder", is_single_value=True)
        with pytest.raises(RuntimeError) as e:
            db.query("SELECT * FROM completedorder", is_df = False, is_single_value=True)
    



if __name__ == "__main__":
    c = TestSQLiteDatabase()
    c.test_getSchema()
    c.test_textSchema()
