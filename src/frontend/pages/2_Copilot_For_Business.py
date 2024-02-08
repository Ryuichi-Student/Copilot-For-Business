import streamlit as st
import pandas as pd
from src.backend.visualisation.PieChart import PieChart
from src.backend.actioner import Actioner
from src.backend.utils.database import SQLiteDatabase

df = pd.DataFrame({'lab':['A', 'X', 'D'], 'val':[10, 30, 20]})

bar = PieChart("title 1", df, "", "lab", "val")
plot = bar.generate()


# title
st.header("Copilot for Business")

# all the user to enter a prompt
userQuery = st.chat_input("Enter your question")


if userQuery:
    # display the user's entered prompt
    st.text(userQuery)

    # get the database
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    # create an actioner object    
    actioner = Actioner(db)

    # get requirements from the actioner
    requirements = actioner.get_requirements(userQuery)

    # for each of the requirements get the required action
    for requirement in requirements:
        action = actioner.get_action(requirement, userQuery)

        # pass actions to the sql generator

        # pass data, query, and actioner parameters to the visualisation

        # go to new page to show plot? allow a keep and delete
        # show code
        # show sql

    # show the answer
    # st.pyplot(plot)



