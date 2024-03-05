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

# header 1 - help
st.header("Help")
st.subheader(":gray[About]")
st.write("Copilot for Business takes your question and uses it with information from the database to try and find the most suitable plot to display an answer. The more specific your query, the more likely Copilot for Business is to be able to come up with an accurate and useful answer. The types of plot available are bar charts, line charts, pie charts and scatter charts.")

# header 2 - sql with explanation of key sql commands
st.subheader(":gray[SQL]")
st.write("When Copilot for Business displays the graph it has generated to answer your question it will give an option to show the SQL used to generate it. This SQL explains which columns from your database have been used and how they have been edited to generate the most suitable graph to answer your question. Here are some key words from an SQL statement and what they mean:")
st.table(sql_commands)

