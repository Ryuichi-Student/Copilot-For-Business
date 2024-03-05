# Use this if you want to test random functions
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from src.backend.visualisation.BarChart import BarChart
import pandas as pd
from src.backend.utils.formatSQL import formatSQL

# Injecting JavaScript to search for elements with specific conditions and apply styles
js = """
<script>
document.querySelectorAll('span').forEach((el) => {
        if (el.textContent == 'Chat') {
            el.style.color = 'yellow';
        }
    });
</script>
"""

st.markdown(js, unsafe_allow_html=True)

prompt = st.chat_input("Say something")

speed = [0.1, 17.5, 40, 48, 52, 69, 88, 12, 23, 45, 11]
lifespan = [2, 8, 70, 1.5, 25, 12, 28, 65, 32, 56, 7]
index = ['snail', 'pig', 'elephant', 'rabbit', 'giraffe', 'coyote', 'horse', 'extra 1', 'extra2', 'extra3', 'extra4']
df = pd.DataFrame({'speed': speed, 'lifespan': lifespan, 'lab' : index})

if True:
    st.write(f"User has sent the following prompt: {prompt}")
    
    chart = BarChart(df, "query", {'title': 'title of the chart', 'x_axis': 'lab', 'y_axis': 'lifespan'})

    chart.query = "SELECT total_amount_spent_on_orders_per_client.client_id, (total_amount_spent_on_orders_per_client.total_amount + total_amount_spent_on_transactions_per_client.total_amount + total_loan_amount_per_client.total_amount) AS total_value FROM total_amount_spent_on_orders_per_client JOIN total_amount_spent_on_transactions_per_client ON total_amount_spent_on_orders_per_client.client_id = total_amount_spent_on_transactions_per_client.client_id JOIN total_loan_amount_per_client ON total_amount_spent_on_orders_per_client.client_id = total_loan_amount_per_client.client_id ORDER BY total_value DESC"

    chart.ascending()
    vis = chart.generate()
    
    st.plotly_chart(vis)
    st.markdown(formatSQL({"some sql" : chart.query}))