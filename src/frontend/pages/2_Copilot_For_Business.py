import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from glob import glob

import streamlit as st
from src.backend.copilot import Copilot
from src.backend.utils.sessions import Session_Storage


def display_session_ui():
    print("Displaying session UI")
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


col1, col2 = st.columns([8, 2])
with col1:
    # title
    st.header("Ask a question")
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
        st.text(f"USER:")
        st.markdown(userQuery)
        st.text("COPILOT FOR BUSINESS:")
        status_placeholder = st.empty()
        status = status_placeholder.status("Thinking...")
        copilot.set_status_placeholder(status)
        copilot.query(userQuery)
        # pass actions to the sql generator

        plot = copilot.get_plot(userQuery)
        answer = copilot.get_answer(userQuery)

        status_placeholder.empty()

        # none type has no attribute formatSQL
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
                plot.formatSQL()

        elif answer:
            st.write(answer)
        
        else:
            st.markdown("Copilot for Business was not able to generate an answer. Please try to refine your command to help")
        


