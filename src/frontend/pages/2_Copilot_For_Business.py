import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import streamlit as st
import pandas as pd
import json
from src.backend.visualisation.PieChart import PieChart
from src.backend.actioner import Actioner
from src.backend.utils.database import SQLiteDatabase
from src.backend.utils.visualiser import get_test_chart


df, bar, plot = get_test_chart()


# TODO: Load from persistent storage
if "session_storage" not in st.session_state:
    st.session_state.session_storage = {}
sessions = st.session_state.session_storage


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

