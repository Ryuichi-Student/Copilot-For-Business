import streamlit as st
from src.backend.utils.sessions import Session_Storage

# TODO: Load from persistent storage
if "session_storage" not in st.session_state:
    st.session_state.session_storage = Session_Storage(st.rerun)
sessions = st.session_state.session_storage

if "CREATE_SESSION" not in st.session_state:
    st.session_state.CREATE_SESSION = False

st.header("Create/Delete Sessions")


if st.button("Create Session"):
    st.session_state.CREATE_SESSION = True

if st.session_state.CREATE_SESSION:
    session_name = st.text_input("Enter a session name.")
    if session_name:
        st.session_state.CREATE_SESSION = False
        sessions.create_session(session_name)

st.write("## Current Sessions")

for session_id in sessions.get_sessions():
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.write(sessions.session_data[session_id]["name"])
    with col2:
        if st.button("X", key=session_id):
            sessions.delete_session(session_id)
