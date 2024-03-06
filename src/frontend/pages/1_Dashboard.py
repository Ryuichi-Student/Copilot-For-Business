import atexit
import pickle
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.backend.database import SQLiteDatabase
from src.backend.utils.sessions import Session_Storage

import streamlit as st
import sqlite3
import os

css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.2rem;
    }
    .st-emotion-cache-1dj0hjr.eczjsme5 {
        color: yellow !important;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

@st.cache_resource()
def get_storage():
    ss = None
    # If a session storage exists in a pickle file, load it instead
    if os.path.exists("session_manager.pkl"):
        try:
            with open("session_manager.pkl", "rb") as f:
                ss = pickle.load(f)
        except:
            ss = None
    if ss is None or not isinstance(ss, Session_Storage):
        ss = Session_Storage(st.rerun)
    else:
        ss.rerun = st.rerun
    return ss


# TODO: Load from persistent storage
if "session_storage" not in st.session_state:
    st.session_state.session_storage = get_storage()
sessions = st.session_state.session_storage

if "CREATE_SESSION" not in st.session_state:
    st.session_state.CREATE_SESSION = False

st.header("Dashboard")

tabs = st.tabs(["Question History", "Upload Database"])
# View the sessions that you have made and delete sessions by clicking the "X" button.
sessions_list = sessions.get_sessions()
x = len(sessions_list)

def run():
    st.write("\n")
    for session_id in sessions_list:
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.write(sessions.session_data[session_id]["name"])
        with col2:
            if st.button("X", key=session_id):
                sessions.delete_session(session_id)
    st.write("\n")

with tabs[0]:
    if x > 6:
        with st.container(height=415, border=False):
            run()
    else:
        with st.container(border=False):
            run()

# Create a new session by clicking a button and entering a session name in the text box that appears
if st.button("Create a new question"):
    st.session_state.CREATE_SESSION = not st.session_state.CREATE_SESSION

if st.session_state.CREATE_SESSION:
    session_name = st.text_input("Enter a session name.")
    if session_name:
        st.session_state.CREATE_SESSION = False
        sessions.create_session(session_name, autogenerate=False)

# TODO: Add undo functionality


st.write("\n")

with tabs[1]:
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
        uploaded_file = st.file_uploader("", type=["sqlite3", "db", "pdf"])

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




@atexit.register
def shutdown():
    # Add session_manager to a pickle file
    with open("session_manager.pkl", "wb") as f:
        print("Saving session manager to session_manager.pkl")
        pickle.dump(sessions, f)
