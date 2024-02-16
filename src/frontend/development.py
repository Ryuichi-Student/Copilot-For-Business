# Use this if you want to test random functions
# TODO: For development purposes only. Use REST APIs or some other communication protocols to interact with backend.
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.backend.visualisation.LineChart import LineChart
from src.backend.database import SQLiteDatabase
from src.backend.test import *

# db = SQLiteDatabase('databases/crm_refined.sqlite3')
# print(db.getTextSchema())

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

    df, chart, _ = get_test_chart()
    st.write(chart.getSQLQuery())
    # command = test_actioner_workflow(prompt)

    # st.write(f"Backend has responded with the following command: {command}")