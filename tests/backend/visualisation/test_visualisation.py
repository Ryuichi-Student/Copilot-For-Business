import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# import bar graph class
from src.backend.visualisation.BarChart import BarChart
# import pie chart class
from src.backend.visualisation.PieChart import PieChart

# tests validation for bar chart
def test_validateBarChart():
    df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
    bar = BarChart("title", df, "query", "lab", "val")
    assert bar.validate()

# test validation from pie chart
def test_validatePieChart():
    df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
    pie = PieChart("title", df, "query", "lab", "val")
    assert pie.validate()
