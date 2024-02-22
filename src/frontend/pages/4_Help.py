import streamlit as st
import pandas as pd

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

commands = ["SELECT", "AS", "FROM", "WHERE", "JOIN"]
description = ["Used to select data from the database. Selects the columns with the subsequent names", 
               "Used to alias a column or table name to make an SQL command more readable", 
               "Used to specify the database the previous columns have been selected from", 
               "Conditions used to filter the records selected by the SELECT statement", 
               "Used to join multiple tables together on a certain column, to fetch data over multiple tables"]
sql_commands = pd.DataFrame({
    "Commands" : commands,
    "Description" : description
})
sql_commands = sql_commands.set_index('Commands')

st.header("Help")

st.header("SQL")
st.write("When Copilot for Business displays the graph it has generated to answer your question it will give an option to show the SQL used to generate it. This SQL explains which columns from your database have been used and how they have been edited to generate the most suitable graph to answer your question. Here are some key words from an SQL statement and what they mean:")
st.table(sql_commands)

