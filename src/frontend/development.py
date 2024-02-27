# Use this if you want to test random functions
# TODO: For development purposes only. Use REST APIs or some other communication protocols to interact with backend.
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
# from src.backend.visualisation.LineChart import LineChart
# from src.backend.database import SQLiteDatabase
from src.backend.test import *

# db = SQLiteDatabase('databases/crm_refined.sqlite3')
# print(db.getTextSchema())

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    
    df, chart, vis = get_test_chart()

    chart.query = "SELECT total_amount_spent_on_orders_per_client.client_id, (total_amount_spent_on_orders_per_client.total_amount + total_amount_spent_on_transactions_per_client.total_amount + total_loan_amount_per_client.total_amount) AS total_value FROM total_amount_spent_on_orders_per_client JOIN total_amount_spent_on_transactions_per_client ON total_amount_spent_on_orders_per_client.client_id = total_amount_spent_on_transactions_per_client.client_id JOIN total_loan_amount_per_client ON total_amount_spent_on_orders_per_client.client_id = total_loan_amount_per_client.client_id ORDER BY total_value DESC"
    # st.write(chart.getSQLQuery())
    # st.plotly_chart(chart.generate())
    chart.formatSQL()
    # command = test_actioner_workflow(prompt)

    # st.write(f"Backend has responded with the following command: {command}")