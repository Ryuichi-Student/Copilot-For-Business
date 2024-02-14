import os, sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

<<<<<<< HEAD
from src.backend.sql.generator import SQLGenerator
from src.backend.database import SQLiteDatabase
=======
from src.backend.sql.generator import SQLGenerator, ResponseError, ResponseNotJSONError, ResponseContentMissingError, ResponseStatusError, Status_COLUMN_NOTIN_SCHEMA_Error, Status_INVALID_ACTION_COMMAND_Error, Status_GRAPH_INFO_NOT_APPLICABLE_Error, InvalidQueryError, QueryValidationError, QueryExecutionError
from src.backend.utils.database import SQLiteDatabase
>>>>>>> 6dcc286e9b5d4214c2a5215cdfb419d62d372441


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


    def test_generate_error_COLUMNNOTINSCHEMA(self):
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

    def test_generate_error_GRAPHINFONOTAPPLICABLE(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        action_command = "To calculate the customer lifetime value (CLV), you will need to aggregate the total revenue generated from each customer over time and possibly factor in the duration of the customer relationship. You can use the completedorder, completedtrans, and completedloan tables to find the total revenue from orders, transactions, and loans respectively. Join these tables with the completedclient table to associate the revenue with individual customers. Optionally, you may also consider the costs associated with servicing the customer, which could be derived from CRM_Events and CRM_Call_Center_Logs if such costs are recorded. Calculate the total revenue per customer and subtract any associated costs to get the CLV. Sort the results by the CLV in descending order to identify the most valuable customers."
        graph_meta = {
            "graph_type": "Samuel",
            "graph_info": {
                "x_axis": "penguin eats banana",
                "y_axis": "love in an open door"
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
        assert response["error"] == "GRAPH_INFO_NOT_APPLICABLE"
    
    def test_generate_error_INVALIDACTIONCOMMAND(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        action_command = "Please paint a picture of a cat using SQL."
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
        assert response["error"] == "INVALID_ACTION_COMMAND"
    
    def test_generate_validate(self):
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
        with pytest.raises(QueryExecutionError) as e:
            gen.validateQuery("SELECT COUNT(*) FRO completedorder")