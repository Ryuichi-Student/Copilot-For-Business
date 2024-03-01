# TODO: use this as home page.
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import streamlit as st
from streamlit_javascript import st_javascript
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Welcome to Copilot For Business! 👋")
st.sidebar.success("")

st.markdown(
    """
    ## What is this?

    
    Copilot for Business is a tool that helps you analyse databases better, faster, and more efficiently. It's powered by OpenAI's GPT-3 and GPT-4 models.
     
    ## What does it do?

    You can ask Copilot for Business questions about your database, and it will help you write SQL queries, explain the results, and more. For example you can ask:
    - "Who are the top 5 customers measured by revenue?"
    - Upon this query, Copilot will generate a SQL query to find the top 5 customers by revenue, create a chart to visualize the results, and explain the results in plain English.
"""

# link to ask a question/try out
# extension: link to see previous queries? 
)


