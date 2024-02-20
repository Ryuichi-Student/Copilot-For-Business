import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.backend.visualisation.BarChart import BarChart
from src.backend.visualisation.PieChart import PieChart
from src.backend.visualisation.LineChart import LineChart
from src.backend.visualisation.ScatterChart import ScatterChart

# tests validation for bar chart
def test_validateBarChart():
    df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
    bar = BarChart(df, "query", {'title': 'title1', 'x_axis': 'lab', 'y_axis': 'val'})
    assert bar.validate()

# test validation for pie chart
def test_validatePieChart():
    df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
    pie = PieChart(df, "query", {'title': 'title1', 'categories': 'lab', 'count': 'val'})
    assert pie.validate()


# test validation for line chart
def test_validateLineChart():
    df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
    line = LineChart(df, "query", {'title': 'title1', 'x_axis': 'lab', 'y_axis': 'val'})
    assert line.validate()


# test validation for scatteer chart
def test_validateScatterChart():
    df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
    scatter = ScatterChart(df, "query", {'title': 'title1', 'x_axis': 'lab', 'y_axis': 'val'})
    assert scatter.validate()