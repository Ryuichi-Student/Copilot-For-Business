import pandas as pd
from src.backend.copilot import Copilot
from src.backend.database import DataFrameDatabase
from src.backend.utils.gpt import get_gpt_response
from src.backend.visualisation.PieChart import PieChart


def dummy_test():
    return "Backend is operational"

def test_api(message_placeholder, prompt = "What is the capital of Japan?"):
    return get_gpt_response(
        ("system", "You are a helpful assistant"),
        ("user", prompt),
        stream=True,
        message_placeholder=message_placeholder
    )

def test_actioner_workflow(query):
    copilot = Copilot()
    copilot.query(query)

def get_test_chart():
    speed = [0.1, 17.5, 40, 48, 52, 69, 88]
    lifespan = [2, 8, 70, 1.5, 25, 12, 28]
    index = ['snail', 'pig', 'elephant', 'rabbit', 'giraffe', 'coyote', 'horse']
    df = pd.DataFrame({'speed': speed, 'lifespan': lifespan, 'lab' : index})

    pie = PieChart(df, "SELECT total_amount_spent_on_orders_per_client.client_id, (total_amount_spent_on_orders_per_client.total_amount + total_amount_spent_on_transactions_per_client.total_amount + total_loan_amount_per_client.total_amount) AS total_value FROM total_amount_spent_on_orders_per_client JOIN total_amount_spent_on_transactions_per_client ON total_amount_spent_on_orders_per_client.client_id = total_amount_spent_on_transactions_per_client.client_id JOIN total_loan_amount_per_client ON total_amount_spent_on_orders_per_client.client_id = total_loan_amount_per_client.client_id ORDER BY total_value DESC", {'title': 'title of the chart', 'categories': 'lab', 'count': 'speed'})
    plot = pie.generate()
    return df, pie, plot