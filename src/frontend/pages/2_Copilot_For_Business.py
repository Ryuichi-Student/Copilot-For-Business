import streamlit as st
import pandas as pd
import json
from src.backend.visualisation.PieChart import PieChart
from src.backend.actioner import Actioner
from src.backend.utils.database import SQLiteDatabase

df = pd.DataFrame({'lab':['A', 'X', 'D'], 'val':[10, 30, 20]})

bar = PieChart("title 1", df, "", "lab", "val")
plot = bar.generate()


# title
st.header("Copilot for Business")

# all the user to enter a prompt
userQuery = st.chat_input("Enter your question")



# put this in a separate function

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
            st.text("wooo yeah")
        else:
            st.text("oh no")
        

        # pass actions to the sql generator

        # pass data, query, and actioner parameters to the visualisation

        # go to new page to show plot? allow a keep and delete
        # show code
        # show sql
            
    # button to allow the user to accept or remove --> a button 

    # show the answer
    # st.pyplot(plot)



def createVisualisation(action):
    # pattern match on the graph_type
    # create a graph of the right type
    # get the bits from the json from the actioner
    pass