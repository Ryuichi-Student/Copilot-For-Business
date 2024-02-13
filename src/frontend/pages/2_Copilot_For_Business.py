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

bar = PieChart("title 1", df, "", "lab", "val")
plot = bar.generate()


# title
st.header("Copilot for Business")

# all the user to enter a prompt
userQuery = st.chat_input("Enter your question")



# put this in a separate file
if userQuery:
    # display the user's entered prompt
    st.text(userQuery)

    # get the database
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    # create an actioner object    
    actioner = Actioner(db)

    # get requirements from the actioner
    requirements = actioner.get_requirements(userQuery)

    st.text(requirements)

    # for each of the requirements get the required action
    for requirement in requirements:
        action = actioner.get_action(requirement, userQuery)
        
        # can only use them for the sql generator if its a success
        if json.loads(action)['status'] == 'success':
            st.text("success")
        else:
            st.text("failure")
        

        # pass actions to the sql generator

        # pass data, query, and actioner parameters to the visualisation

        # go to new page to show plot? allow a keep and delete
        # show code
        # show sql
            
    # button to allow the user to accept or remove --> a button 

    # show the answer
    # st.pyplot(plot)



def createVisualisation(action):
    graph_type = action['graph_type']
    if graph_type == PieChart.getChartName():
        # pie chart object
        # get stuff from actioner
        pass
    elif graph_type == BarChart.getChartName():
        # bar chart object
        pass
    elif graph_type == LineChart.getChartName():
        # line chart object
        pass
    else:
        # other
        pass