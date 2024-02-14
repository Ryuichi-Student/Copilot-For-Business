import streamlit as st
import pandas as pd
from src.backend.visualisation.PieChart import PieChart
from src.backend.visualisation.LineChart import LineChart
from src.backend.visualisation.BarChart import BarChart
from src.frontend.pages.workflow import workflow

df = pd.DataFrame({'lab':['A', 'X', 'D'], 'val':[10, 30, 20]})

pie = PieChart("title 1", df, "SELECT * FROM *", "lab", "val")

state = st.session_state

if "chart" not in state:
    state["chart"] = False


# title
st.header("Copilot for Business")

# all the user to enter a prompt
state['userQuery'] = st.chat_input("Enter your question")



# put this in a separate file
if state['userQuery']:
    # display the user's entered prompt
    st.text(state['userQuery'])

    workflow(state["userQuery"])
    # start the workflow
    state["chart"] = True



# TESTING!!! change showChart function probably
# if there's an outputted graph show it
if state["chart"]:
    # have the visualisation object
    plot = pie.generate()

    sqlView = st.toggle("Show SQL query")
    if sqlView:
        st.write(pie.getSQLQuery())


