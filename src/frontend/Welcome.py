# TODO: use this as home page.
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import streamlit as st
from streamlit_javascript import st_javascript
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Welcome to Copilot For Business! 👋")
st.sidebar.success("")

st.write("Welcome to Copilot for Business. This is a student run project at the University of Cambridge, in collaboration with Cambridge Kinematics. This project is part of the second year project in the Computer Science Tripos. ")
st.write("The team: Samuel Jie, Isaac Lam, Izzi Millar, Mmesoma Okoro, Leo Takashige and Ram Vinjamuri.")

st.markdown(
    """
    ## What have we built?

    
    Copilot for Business is a tool that helps you analyse databases better, faster, and more efficiently. It's powered by OpenAI's GPT-3 and GPT-4 models.
     
    ## What does it do?

    You can ask Copilot for Business questions about your database, and it will help you write SQL queries, explain the results, and more. For example you can ask:
    - "Who are the top 5 customers measured by revenue?"
    - Upon this query, Copilot will generate a SQL query to find the top 5 customers by revenue, create a chart to visualize the results, and explain the results in plain English.
"""

# link to ask a question/try out
# extension: link to see previous queries? 
)

st.write("## Try it out!")



st.write("To start you can either go to the dashboard to upload your database or go to the main page (copilot for business) in order to start using the app. If you need help at any point, please consult the help page.")
st.markdown("[Click here to try now!!!](/Copilot_For_Business)")

st.write("Below is an example of how you can ask Copilot for Business a question. Try it out! This is for the example database crm_refined. Feel free to try the example yourself by clicking on the Copilot For Business tab on the left.")

# Send to copilot page, forward
link_style = """
border-color: #007bff;
align: center;
text-align: right;
display: block;
border-right: 100px ;

"""

# Toggle for light/dark mode
dark = st.toggle("Dark Mode Example", True)

# If toggle clicked
if dark:
    st.image("Dark_Example.png", use_column_width=True)
else:
    st.image("Light_Example.png", use_column_width=True)

