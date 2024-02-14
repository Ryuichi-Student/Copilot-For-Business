import pandas as pd

from src.backend.visualisation.PieChart import PieChart

def get_test_chart():
    df = pd.DataFrame({'lab': ['A', 'X', 'D'], 'val': [10, 30, 20]})

    bar = PieChart("title 1", df, "", "lab", "val")
    plot = bar.generate()
    return df, bar, plot

