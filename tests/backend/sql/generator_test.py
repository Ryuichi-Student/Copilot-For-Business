import sqlite3 as sql
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.backend.sql.generator import SQLGenerator
from src.backend.utils.database import SQLiteDatabase


class TestSQLGenerator:
    def test_generate_case1(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        action_command = "To calculate the customer lifetime value (CLV), you will need to aggregate the total revenue generated from each customer over time and possibly factor in the duration of the customer relationship. You can use the completedorder, completedtrans, and completedloan tables to find the total revenue from orders, transactions, and loans respectively. Join these tables with the completedclient table to associate the revenue with individual customers. Optionally, you may also consider the costs associated with servicing the customer, which could be derived from CRM_Events and CRM_Call_Center_Logs if such costs are recorded. Calculate the total revenue per customer and subtract any associated costs to get the CLV. Sort the results by the CLV in descending order to identify the most valuable customers."
        graph_meta = {
            "graph_type": "Bar",
            "graph_info": {
                "x_axis": "client_id",
                "y_axis": "lifetime_value"
            }
        }
        rele_cols = [
            "completedorder.account_id",
            "completedorder.amount",
            "completedtrans.account_id",
            "completedtrans.amount",
            "completedloan.account_id",
            "completedloan.payments",
            "completedclient.client_id",
        ]
        gen = SQLGenerator(db, actionCommand=action_command, graph_info=graph_meta, relevantColumns=rele_cols)
        response = gen.generateQuery()
        print(response)
        assert isinstance(response, dict)
        assert response["status"] == "success"


    def test_generate_error(self):
        relative_path = "databases/crm_refined_droppedtable.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        action_command = "To calculate the customer lifetime value (CLV), you will need to aggregate the total revenue generated from each customer over time and possibly factor in the duration of the customer relationship. You can use the completedorder, completedtrans, and completedloan tables to find the total revenue from orders, transactions, and loans respectively. Join these tables with the completedclient table to associate the revenue with individual customers. Optionally, you may also consider the costs associated with servicing the customer, which could be derived from CRM_Events and CRM_Call_Center_Logs if such costs are recorded. Calculate the total revenue per customer and subtract any associated costs to get the CLV. Sort the results by the CLV in descending order to identify the most valuable customers."
        graph_meta = {
            "graph_type": "Bar",
            "graph_info": {
                "x_axis": "client_id",
                "y_axis": "lifetime_value"
            }
        }
        rele_cols = [
            "completedorder.account_id",
            "completedorder.amount",
            "completedtrans.account_id",
            "completedtrans.amount",
            "completedloan.account_id",
            "completedloan.payments",
            "completedclient.client_id",
        ]
        gen = SQLGenerator(db, actionCommand=action_command, graph_info=graph_meta, relevantColumns=rele_cols)
        response = gen.generateQuery()
        print(response)
        assert isinstance(response, dict)
        assert response["status"] == "error"
        assert response["error"] == "COLUMN_NOTIN_SCHEMA"