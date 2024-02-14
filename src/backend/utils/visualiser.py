import pandas as pd

from src.backend.visualisation.PieChart import PieChart

def get_test_chart():
    df = pd.DataFrame({'lab': ['A', 'X', 'D'], 'val': [10, 30, 20]})

    pie = PieChart("title 1", df, "SELECT * FROM *", "lab", "val")
    plot = pie.generate()
    return df, pie, plot

