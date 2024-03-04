import pandas as pd
from src.backend.copilot import Copilot
from src.backend.database import DataFrameDatabase
from src.backend.utils.gpt import get_gpt_response
from src.backend.visualisation.BarChart import BarChart


def dummy_test():
    return "Backend is operational"

def test_api(message_placeholder, prompt = "What is the capital of Japan?"):
    return get_gpt_response(
        ("system", "You are a helpful assistant"),
        ("user", prompt),
        gpt4 = False,
        stream=True,
        message_placeholder=message_placeholder
    )

def test_actioner_workflow(query):
    copilot = Copilot()
    copilot.query(query)

def get_test_chart():
    speed = [0.1, 17.5, 40, 48, 52, 69, 88, 12, 23, 45, 11]
    lifespan = [2, 8, 70, 1.5, 25, 12, 28, 65, 32, 56, 7]
    index = ['snail', 'pig', 'elephant', 'rabbit', 'giraffe', 'coyote', 'horse', 'extra 1', 'extra2', 'extra3', 'extra4']
    df = pd.DataFrame({'speed': speed, 'lifespan': lifespan, 'lab' : index})

    pie = BarChart(df, "query", {'title': 'title of the chart', 'x_axis': 'lab', 'y_axis': 'lifespan'})
    plot = pie.generate()
    return df, pie, plot