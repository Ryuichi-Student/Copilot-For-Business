import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.backend.database import SQLiteDatabase
from src.backend.utils.sessions import Session_Storage

import streamlit as st
import sqlite3
import os

# TODO: Load from persistent storage
if "session_storage" not in st.session_state:
    st.session_state.session_storage = Session_Storage(st.rerun)
sessions = st.session_state.session_storage

if "CREATE_SESSION" not in st.session_state:
    st.session_state.CREATE_SESSION = False

st.header("Create/Delete Sessions")


# Create a new session by clicking a button and entering a session name in the text box that appears
if st.button("Create Session"):
    st.session_state.CREATE_SESSION = True

if st.session_state.CREATE_SESSION:
    session_name = st.text_input("Enter a session name.")
    if session_name:
        st.session_state.CREATE_SESSION = False
        sessions.create_session(session_name)

# View the sessions that you have made and delete sessions by clicking the "X" button.
st.write("## Current Sessions")

for session_id in sessions.get_sessions():
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.write(sessions.session_data[session_id]["name"])
    with col2:
        if st.button("X", key=session_id):
            sessions.delete_session(session_id)

# TODO: Add undo functionality


upload_status, upload_end, table_name = 0, 0, ""


def upload_progress(args, upload_placeholder=None, upload_placeholder2=None):
    global upload_status, upload_end, table_name
    if len(args) == 2:
        upload_status, upload_end = args
        if upload_status == upload_end:
            upload_status = 0
            upload_end = 0
            upload_placeholder.empty()
            upload_placeholder2.empty()
        print(upload_status, upload_end)
    else:
        upload_status += 1
        table_name = args
        print(upload_status, upload_end)
    if upload_end:
        upload_placeholder.progress(upload_status/upload_end)
        upload_placeholder2.write(f"Analyzing table: {table_name}")

# Upload a database file


def get_db_upload():
    uploaded_file = st.file_uploader("Choose a file", type=["sqlite3", "db", "pdf"])

    if uploaded_file is not None:

        file_content = uploaded_file.read()
    
        # Check if file already exists
        condition = True
        count = 2
        while condition:
            # if file exists
            if os.path.exists(f"uploads/{uploaded_file.name}"):
                uploaded_file.name = f"{uploaded_file.name.split('.')[0]}_{count}.{uploaded_file.name.split('.')[1]}"
                count += 1
            else:
                condition = False

        with open(f"uploads/{uploaded_file.name}", "wb") as f:
            f.write(file_content)

        try:
            # Open the file with sqlite3
            conn = sqlite3.connect(f"uploads/{uploaded_file.name}")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print("Connected")
            conn.close()

            # Preprocess Sqlite3 database
            upload_placeholder = st.empty()
            upload_placeholder.progress(0)
            upload_placeholder2 = st.empty()
            SQLiteDatabase(f"uploads/{uploaded_file.name}", progress_callback=lambda args: upload_progress(args, upload_placeholder, upload_placeholder2))
            st.success(f"Saved {uploaded_file.name} to uploads folder")

        except Exception as e:
            st.error(f"Failed to save {uploaded_file.name} to databases folder")
            st.error("Please upload a valid sqlite3 database file")
            conn.close()
            print(e)
            # Delete the file
            os.remove(f"uploads/{uploaded_file.name}")


get_db_upload()