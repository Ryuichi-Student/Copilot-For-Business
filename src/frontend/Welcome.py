# TODO: use this as home page.
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import streamlit as st
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Welcome to Copilot For Business! 👋")
st.sidebar.success("")

st.markdown(
    """
    ## What is this?
    - 
    ## What does it do?
    - 
"""

# need explanation about what this product is and what it does ? 
# link to ask a question/try out
# extension: link to see previous queries? 
)
