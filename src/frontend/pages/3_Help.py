import streamlit as st
import pandas as pd
from streamlit_player import st_player

import os, sys


st.markdown("""
<style>
    .st-emotion-cache-1dj0hjr.eczjsme5 {
        color: yellow !important;
    }
    
</style>
""", unsafe_allow_html=True)
st.markdown("""
  <style>
     /* Streamlit class name of the div that holds the expander's title*/
    .st-emotion-cache-sh2krr.e1nzilvr5 p {
      font-size: 17px;
      color: #e092f0;
      }
  </style>
""", unsafe_allow_html=True)


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

commands = ["SELECT", "AS", "FROM", "WHERE", "JOIN"]
description = ["Used to select data from the database. Selects the columns with the subsequent names", 
               "Used to alias a column or table name to make an SQL command more readable", 
               "Used to specify the database the previous columns have been selected from", 
               "Conditions used to filter the records selected by the SELECT statement", 
               "Used to join multiple tables together on a certain column, to fetch data over multiple tables"]
sql_commands = pd.DataFrame({
    "Commands" : commands,
    "Description" : description
})
sql_commands = sql_commands.set_index('Commands')

# header 1 - help
st.header("Help")
st.subheader(":gray[About]")
st.write("Copilot for Business takes your question and uses it with information from the database to try and find the most suitable plot to display an answer. The more specific your query, the more likely Copilot for Business is to be able to come up with an accurate and useful answer. The types of plot available are bar charts, line charts, pie charts and scatter charts.")

# header 2 - sql with explanation of key sql commands
st.subheader(":gray[FAQs]")


with st.expander("How do I use this app?", expanded=True):
    st.write("We have a quick tutorial!")
    st_player("https://youtu.be/vAk7c7Ye0BE")


with st.expander("What does all this SQL mean?"):
    st.write("When Copilot for Business displays the graph it has generated to answer your question it will give an option to show the SQL used to generate it. This SQL explains which columns from your database have been used and how they have been edited to generate the most suitable graph to answer your question. Here are some key words from an SQL statement and what they mean:")
    st.table(sql_commands)


with st.expander("How much better is this than asking ChatGPT 4?"):
    st.markdown("Copilot for Business is an entire pipeline which incorporates finetuned GPT-3.5 and GPT-4 models and our own functions. This allows Copilot For Business to understand your data unlike no other easily available alternatives.")
    st.markdown("Let's compare ChatGPT 4 and Copilot for Business:")
    st.image("src/frontend/images/ChatGPT4Fail.png", use_column_width=True)
    st.write("ChatGPT4 is the state-of-the-art LLM provided by OpenAI to users for £20 a month. It cannot directly analyse SQLite3 files, so it attempts to write Python to query it. While it is one of the best LLMs the public has access to, it falls short in specialised tasks such as querying databases. After a very long and unreliable upload time, ChatGPT fails to understand the database it is given and wastes the user's time retrying fruitlessly until the dreaded network error! No graph is provided and the explanation is both wrong and too technical.")
    st.image("src/frontend/images/Dark_Example.png", use_column_width=True)
    st.write("Meanwhile, Copilot for Business understands the context of the database and is able to answer the question in a precise and easy-to-understand manner; an accompanying visualisation is provided, as well as SQL for the more technical. If the database does not contain the necessary information, Copilot for Business does not waste the user's time and instead provides a clear explanation of the problem.")
    st.write("Copilot is up to 10x faster than ChatGPT 4 before providing an answer, and is immeasurably more accurate and reliable (in testing, GPT4 was unable to answer a single question adequately on a large database).")


with st.expander("I missed your presentation, can I see it?"):
    st.write("Of course! Here it is:")
    st_player("https://youtu.be/S09kbiUEAYU")
