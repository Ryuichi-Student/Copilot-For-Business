import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import streamlit as st
import json
from src.backend.copilot import Copilot
from src.backend.test import get_test_chart
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


col1, col2 = st.columns([8, 2])
with col1:
    # title
    st.header("Copilot for Business")
with col2:
    # Session data
    # TODO: Load from persistent storage
    if "session_storage" not in st.session_state:
        st.session_state.session_storage = Session_Storage(st.rerun)
    current_session_id, copilot = display_session_ui()


if current_session_id is not None:
    # Extend to being more of a chat or asking the same copilot a question.
    if copilot.UserQueries:
        # Get a random question from the user queries for now
        userQuery = copilot.get_random_query().userQuery
    else:
        userQuery = st.chat_input("Enter your question")

    if userQuery:
        # TODO: Do more formatting
        # display the user's entered prompt
        st.text(f"USER:\n{userQuery}\n\nCOPILOT:")

        copilot.query(userQuery)
        # pass actions to the sql generator

        # pass data, query, and actioner parameters to the visualisation

        # go to new page to show plot? allow a keep and delete
        # show code
        # show sql

        # button to allow the user to accept or remove --> a button

        plot = copilot.get_plot(userQuery)
        answer = copilot.get_answer(userQuery)
        if plot:
            st.pyplot(plot)
        if answer:
            st.write(answer)

