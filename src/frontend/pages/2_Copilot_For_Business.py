import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import streamlit as st
import json
from src.backend.copilot import Copilot
from src.backend.utils.visualiser import get_test_chart
from src.backend.utils.sessions import Session_Storage


df, bar, plot = get_test_chart()


def display_session_ui():
    session_manager = st.session_state.session_storage
    sessions = session_manager.get_sessions()

    if not sessions:
        st.write("No sessions available")
        current_session_id = None
        copilot = None
    else:
        current_session_id = st.selectbox(
            label="Select a session:",
            options=sessions,
            format_func=lambda x: session_manager.get_session_data(x)['name'],
            index=0  # Automatically switch to the most recent session ID
        )
        copilot = session_manager.get_session_data(current_session_id)['data']
        if copilot is None:
            # TODO: Choose what databases to allow the model to retrieve data from
            copilot = Copilot(db='databases/crm_refined.sqlite3', dbtype='sqlite')
            session_manager.update_session_data(current_session_id, data=copilot)
        else:
            session_manager.update_session_data(current_session_id)
    print(f"New session: {current_session_id}")
    return current_session_id, copilot


# title
st.header("Copilot for Business")


# Session data
# TODO: Load from persistent storage
if "session_storage" not in st.session_state:
    st.session_state.session_storage = Session_Storage(st.rerun)
current_session_id, copilot = display_session_ui()


if current_session_id is not None:
    # all the user to enter a prompt
    userQuery = st.chat_input("Enter your question")


    # put this in a separate file
    if userQuery:
        # display the user's entered prompt
        st.text(userQuery)

        copilot.query(userQuery)

        st.text(copilot.get_requirements(userQuery))

        # for each of the requirements get the required action
        for action in copilot.get_actionCommands(userQuery):
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

