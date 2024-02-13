import streamlit as st
import pandas as pd
import json
from src.backend.visualisation.PieChart import PieChart
from src.backend.visualisation.LineChart import LineChart
from src.backend.visualisation.BarChart import BarChart
from src.backend.actioner import Actioner
from src.backend.utils.database import SQLiteDatabase
from src.backend.visualisation import visualisation_subclasses

df = pd.DataFrame({'lab':['A', 'X', 'D'], 'val':[10, 30, 20]})

pie = PieChart("title 1", df, "SELECT * FROM *", "lab", "val")

state = st.session_state

if "chart" not in state:
    state["chart"] = False


# title
st.header("Copilot for Business")

# all the user to enter a prompt
userQuery = st.chat_input("Enter your question")



# put this in a separate file
if userQuery:
    # display the user's entered prompt
    st.text(userQuery)
    
    # start the workflow
    st.session_state["chart"] = True



# TESTING!!! change showChart function probably
# if there's an outputted graph show it
if state["chart"]:
    # have the visualisation object
    plot = pie.generate()

    sqlView = st.toggle("Show SQL query")
    if sqlView:
        st.write(pie.getSQLQuery())


