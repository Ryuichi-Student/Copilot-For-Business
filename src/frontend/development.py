# Use this if you want to test random functions
# TODO: For development purposes only. Use REST APIs or some other communication protocols to interact with backend.
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.backend.test import *

test_db()

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    gpt_box = st.empty()
    test_api(gpt_box, prompt)

st.write(f"{dummy_test()}")