import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from glob import glob

import streamlit as st
from src.backend.copilot import Copilot
from src.backend.utils.sessions import Session_Storage
from datetime import datetime

if "set_name" not in st.session_state:
    st.session_state.set_name = False
if "userQueryCache" not in st.session_state:
    st.session_state.userQueryCache = None

def display_session_ui():
    print("Displaying session UI")
    session_manager = st.session_state.session_storage
    sessions = session_manager.get_sessions()

    if session_manager.requires_autogenerated_session:
        session_manager.create_session(f"New Session {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", rerun=False)
        sessions = session_manager.get_sessions()
        session_manager.get_session_data(sessions[-1])["autogenerate"] = True

    current_session_id = st.selectbox(
        label="Select a session:",
        options=sessions,
        format_func=lambda x: session_manager.get_session_data(x)['name'],
        index=0  # Automatically switch to the most recent session ID
    )  # type: ignore

    current_session = session_manager.get_session_data(current_session_id)

    if "autogenerate" in current_session and current_session["autogenerate"]:
        st.session_state.set_name = True

    copilot = current_session['data']

    if copilot is None:
        # TODO: Choose what databases to allow the model to retrieve data from

        list_of_databases = glob("databases/*.sqlite3")
        list_of_databases.extend(glob("databases/*.db"))

        list_of_databases.extend(glob("uploads/*.sqlite3"))
        list_of_databases.extend(glob("uploads/*.db"))

        # Should make this more dynamic
        latest_db = max(list_of_databases, key=os.path.getctime)
        print(f"Loading database: {latest_db}")

        st.write(f"Loading database: {latest_db}")

        copilot = Copilot(db=latest_db, dbtype='sqlite')
        session_manager.update_session_data(current_session_id, data=copilot)
    else:
        session_manager.update_session_data(current_session_id)
    print(f"New session: {current_session_id}")
    return current_session_id, copilot


col1, col2 = st.columns([7, 3])

with col2:
    # Session data
    # TODO: Load from persistent storage
    if "session_storage" not in st.session_state:
        st.session_state.session_storage = Session_Storage(st.rerun)
    current_session_id, copilot = display_session_ui()
with col1:
    # title
    st.header("Copilot for Business")
    st.subheader(st.session_state.session_storage.get_session_data(current_session_id)["name"])

session_manager = st.session_state.session_storage

if current_session_id is not None:
    # Extend to being more of a chat or asking the same copilot a question.
    if st.session_state.userQueryCache is not None:
        userQuery = st.session_state.userQueryCache
        st.session_state.userQueryCache = None
    elif copilot.UserQueries:
        # Get a random question from the user queries for now
        userQuery = copilot.get_random_query().userQuery
    else:
        userQuery = st.chat_input("Enter your question")

    if userQuery:
        # TODO: Do more formatting
        if st.session_state.set_name:
            st.session_state.set_name = False
            session_manager.get_session_data(current_session_id)["autogenerate"] = False
            st.session_state.userQueryCache = userQuery
            placeholder = st.empty()
            for x in session_manager.update_session_name(current_session_id, userQuery):
                placeholder.text(x)
            placeholder.empty()
            st.rerun()

        # display the user's entered prompt
        st.text(f"USER:\n{userQuery}\n\nCOPILOT:")

        status_placeholder = st.empty()
        status = status_placeholder.status("Thinking...")
        copilot.set_status_placeholder(status)
        copilot.query(userQuery)

        # button to allow the user to accept or remove

        if copilot.get_early_answer(userQuery):
            st.write(copilot.get_early_answer(userQuery))

        plot = copilot.get_plot(userQuery)

        status_placeholder.empty()

        if plot:
            fig = plot.generate()
            config = {'displayModeBar': None}

            # displays the chart created
            st.plotly_chart(fig, config=config)

            # adds a toggle to show the top 10 values of the dataframe only
            if plot.dfLength > 10:
                topN = st.toggle("Show top 10 values only", False)
                if topN: plot.topn(10, topN)
                else: plot.topn(10, topN)

        sqlView = st.toggle("Show SQL", False)
        if sqlView:
            st.write(copilot.get_sql(userQuery))
            if plot:
                plot.formatSQL()

        if copilot.get_generalised_answer(userQuery):
            st.write(copilot.get_generalised_answer(userQuery))
