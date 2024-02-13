import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.backend.test import *


sessions = st.session_state.session_storage


prompt = st.chat_input("Hi, I'm Copilot For Business. How can I help you with your data today?")
if prompt:
    st.write(f"{prompt}")
    command = test_actioner_workflow(prompt)


    st.write(f"Backend has responded with the following command: {command}")