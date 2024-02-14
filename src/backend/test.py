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
    df = pd.DataFrame({'lab': ['A', 'X', 'D'], 'val': [10, 30, 20]})

    bar = PieChart(df, "", {'title': 'title1', 'categories': 'lab', 'count': 'val'})
    plot = bar.generate()
    return df, bar, plot