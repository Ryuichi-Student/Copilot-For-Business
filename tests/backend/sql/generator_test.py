import os, sys
import pytest
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.backend.sql.generator import SQLGenerator, ResponseError, ResponseNotJSONError, ResponseContentMissingError, ResponseStatusError, Status_COLUMN_NOTIN_SCHEMA_Error, Status_INVALID_ACTION_COMMAND_Error, Status_GRAPH_INFO_NOT_APPLICABLE_Error, InvalidQueryError, QueryValidationError, QueryExecutionError
from src.backend.database import SQLiteDatabase


class TestSQLGenerator:
    def test_generate_case1(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        action_command = "To calculate the customer lifetime value (CLV), you will need to aggregate the total revenue generated from each customer over time and possibly factor in the duration of the customer relationship. You can use the completedorder, completedtrans, and completedloan tables to find the total revenue from orders, transactions, and loans respectively. Join these tables with the completedclient table to associate the revenue with individual customers. Optionally, you may also consider the costs associated with servicing the customer, which could be derived from CRM_Events and CRM_Call_Center_Logs if such costs are recorded. Calculate the total revenue per customer and subtract any associated costs to get the CLV. Sort the results by the CLV in descending order to identify the most valuable customers."
        graph_meta = {
            "graph_type": "Bar Chart",
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
        gen = SQLGenerator(db, actionCommand=action_command, relevantColumns=rele_cols, graph_info=graph_meta)
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
            "graph_type": "Bar Chart",
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
        gen = SQLGenerator(db, actionCommand=action_command, relevantColumns=rele_cols, graph_info=graph_meta)
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
        gen = SQLGenerator(db, actionCommand=action_command, relevantColumns=rele_cols, graph_info=graph_meta)
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
            "graph_type": "Bar Chart",
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
        gen = SQLGenerator(db, actionCommand=action_command, relevantColumns=rele_cols, graph_info=graph_meta)
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
            "graph_type": "Bar Chart",
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
        gen = SQLGenerator(db, actionCommand=action_command, relevantColumns=rele_cols, graph_info=graph_meta)
        with pytest.raises(QueryExecutionError) as e:
            gen.validateQuery("SELECT COUNT(*) FRO completedorder")

    def test_gen_is_single_value(self):
        relative_path = "databases/crm_refined.sqlite3"
        absolute_path = os.path.abspath(os.path.join(relative_path))
        db = SQLiteDatabase(absolute_path)
        graph_meta = {
            "graph_type": "NoChart",
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
        gen = SQLGenerator(db, actionCommand="Calculate the average payment amount for loans.", graph_info=graph_meta, relevantColumns=rele_cols)
        gen._parseQuery(gen.generateQuery())
        assert gen.is_single_value == True
        gen = SQLGenerator(db, actionCommand="Get account IDs and amounts for all completed orders.", graph_info=graph_meta, relevantColumns=rele_cols)
        gen._parseQuery(gen.generateQuery())
        assert gen.is_single_value == False
    
    def test_parse_query(self):
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
        with pytest.raises(ResponseNotJSONError) as e:
            gen._parseQuery("This is a string")
        with pytest.raises(ResponseContentMissingError) as e:
            gen._parseQuery({})
        with pytest.raises(ResponseContentMissingError) as e:
            gen._parseQuery({"status": "success"})
        with pytest.raises(ResponseContentMissingError) as e:
            gen._parseQuery({"status": "success","query": "SELECT * FROM table"})
        with pytest.raises(ResponseContentMissingError) as e:
            gen._parseQuery({"status": "error"})
        with pytest.raises(Status_COLUMN_NOTIN_SCHEMA_Error) as e:
            gen._parseQuery({"status": "error","error": "COLUMN_NOTIN_SCHEMA","message": "Column not found in schema."})
        with pytest.raises(Status_INVALID_ACTION_COMMAND_Error) as e:
            gen._parseQuery({"status": "error","error": "INVALID_ACTION_COMMAND","message": "Invalid action command."})
        with pytest.raises(Status_GRAPH_INFO_NOT_APPLICABLE_Error) as e:
            gen._parseQuery({"status": "error","error": "GRAPH_INFO_NOT_APPLICABLE","message": "Graph info not applicable."})
        assert gen._parseQuery({"status": "success","query": "SELECT * FROM users WHERE user_id = 1","is_single_value": "True"}) == "SELECT * FROM users WHERE user_id = 1"

    def test_validate_query(self):
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
            gen.validateQuery("SELECT * FROM does_not_exist")
        gen.is_single_value = True
        with pytest.raises(ValueError) as e:
            gen.validateQuery("SELECT account_id,amount FROM completedorder")

    def test_execute_query(self):
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
        assert isinstance(gen.executeQuery("SELECT * FROM completedloan WHERE account_id = 'specific_account_id'"), (pd.DataFrame))
        assert isinstance(gen.executeQuery("SELECT * FROM CRM_Events WHERE Product = 'specific_product' ORDER BY Date_received DESC LIMIT 5"), (pd.DataFrame))
        assert isinstance(gen.executeQuery("SELECT * FROM completedclient WHERE client_id = 'specific_client_id'"), (pd.DataFrame))
        assert isinstance(gen.executeQuery("SELECT * FROM CRM_Call_Center_Logs WHERE priority > 8"), (pd.DataFrame))
        assert isinstance(gen.executeQuery("SELECT * FROM completedacct WHERE district_id = (SELECT district_id FROM completeddistrict WHERE city = 'specific_city')"), (pd.DataFrame))
        gen.is_single_value=True
        assert isinstance(gen.executeQuery("SELECT COUNT(*) FROM completedloan"), (int, np.int64, float, np.float64, str))
        assert isinstance(gen.executeQuery("SELECT MAX(funded_amount) FROM LuxuryLoanPortfolio"), (int, np.int64, float, np.float64, str))
        assert isinstance(gen.executeQuery("SELECT AVG(interest_rate_percent) FROM LuxuryLoanPortfolio"), (int, np.int64, float, np.float64, str))
        assert isinstance(gen.executeQuery("SELECT MIN(parseddate) FROM completedacct"), (int, np.int64, float, np.float64, str))
        assert isinstance(gen.executeQuery("SELECT COUNT(*) FROM completedloan"), (int, np.int64, float, np.float64, str))

    