# Use this if you want to test random functions
# TODO: For development purposes only. Use REST APIs or some other communication protocols to interact with backend.
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.backend.test import *

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    test_actioner_workflow(prompt)
    st.write(f"Backend has responded with the following prompt: {dummy_test()}")

st.write(f"{dummy_test()}")