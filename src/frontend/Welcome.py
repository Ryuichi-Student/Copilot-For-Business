# TODO: use this as home page.
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import streamlit as st


st.markdown("""
<style>
    .st-emotion-cache-1dj0hjr.eczjsme5 {
        color: #ffbd45 !important;
    }
</style>
""", unsafe_allow_html=True)


# from streamlit_javascript import st_javascript
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Welcome to Copilot For Business! 👋")
# st.sidebar.success("")

st.write("Welcome to Copilot for Business. This is a student run project at the University of Cambridge, in collaboration with Cambridge Kinetics. This project is part of the second year project in the Computer Science Tripos. ")
st.write("The team: Samuel Jie, Isaac Lam, Izzi Millar, Mmesoma Okoro, Leo Takashige and Ram Vinjamuri.")

st.markdown(
    """
    ## :gray[What is Copilot for Business?]

    
    Copilot for Business is a tool that helps you analyse databases better, faster, and more efficiently. It's powered by OpenAI's GPT-3 and GPT-4 models.
     
    ### :gray[What does it do?]

    You can ask Copilot for Business questions about your database, and it will help you write SQL queries, explain the results, and more. For example you can ask:
    - "Who are the top 5 customers measured by revenue?"
    
    Copilot for business will generate an SQL query to find the top 5 customers by revenue, create a chart to visualize the results, and explain the results in natural language.

    ### :gray[How do I use it?]
    - To upload a database go to 'Dashboard'
    - To ask a question go to 'Copilot for Business'. This will automatically create a "session" which allows you to ask a question. To ask another question or go back to previous sessions, choose from the dropdown in the sidebar.
    - If you are not sure about the database, feel free to ask 'What questions can I ask about the database?'
    - For more help go to 'Help'
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
    st.image("src/frontend/images/Dark_Example.png", use_column_width=True)
else:
    st.image("src/frontend/images/Light_Example.png", use_column_width=True)

