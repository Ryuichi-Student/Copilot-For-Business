import streamlit as st

sessions = st.session_state.session_storage

st.header("Create/Delete Sessions")

def create_session():
    session_name = st.text_input("Enter a session name.")
    if session_name:
        session_id = hash(session_name)
        sessions[session_id] = {"data": ""}
        print(f"Session {session_id} has been created")
        return session_id

def delete_session(session_id):
    if session_id in sessions:
        del sessions[session_id]
        return True
    return False


if st.button("Create Session"):
    session_id = create_session()

