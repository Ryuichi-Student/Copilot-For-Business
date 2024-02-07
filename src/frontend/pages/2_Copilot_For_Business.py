import streamlit as st
import pandas as pd
from src.backend.visualisation.BarChart import BarChart

df = pd.DataFrame({'lab':['A', 'X', 'D'], 'val':[10, 30, 20]})

bar = BarChart("title 1", df, "", "lab", "val")
plot = bar.generate()


# title
st.header("Copilot for Business")

# all the user to enter a prompt
prompt = st.chat_input("Enter your question")


if prompt:
    # display the user's entered prompt
    st.text(prompt)

    # TODO: generate the answer

    # show the answer
    st.pyplot(plot)



