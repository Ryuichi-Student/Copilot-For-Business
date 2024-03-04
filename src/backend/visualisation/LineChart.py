import matplotlib.pyplot as plot
import pandas as pd
import plotly.express as px

# for running this file only
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.backend.visualisation.Visualisation import Visualisation
from src.backend.utils.clean_name import natural_name

class LineChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)
        self.title = info['title']
        self.x_axis = info['x_axis']
        self.y_axis = info['y_axis']
    
    @staticmethod
    def getChartName():
        return "Line chart"
    
    @staticmethod
    def getChartDescription():
        return "This should be chosen when a line chart is most suitable to represent the data, for example to display continuous numerical data or change over time."

    @staticmethod
    def getChartParametersForActioner():
        return {'title': '', 'x_axis': '', 'y_axis': ''}
        
    @staticmethod
    def getChartParameterDescription():
        return "'title' should contain a string of most suitable title for the line chart. 'x_axis' should contain a string of the column name that should be used as the x axis of the line chart. 'y_axis' should contain a string of the column name that should be used as the y axis of the line chart."

    # sets the database to show the top n values by y axis depending on a bool
    def topn(self, n):
        if n == len(self.y_axis):
            self.df = self.modifiedDFs["data"]
        else:
            if n not in self.modifiedDFs:
                self.modifiedDFs[n] = self.modifiedDFs["data"].nlargest(n, self.y_axis).sort_values(by=self.x_axis)
            self.df = self.modifiedDFs[n]
    
    # creates a dataframe with y values in ascending order
    def ascending(self):
        if "ascending" not in self.modifiedDFs:
            self.modifiedDFs["ascending"] = self.modifiedDFs["data"].sort_values(by=self.y_axis)
        
        self.df = self.modifiedDFs["ascending"]


    def descending(self):
        if "descending" not in self.modifiedDFs:
            self.modifiedDFs["descending"] = self.modifiedDFs["data"].sort_values(by=self.y_axis)
        
        self.df = self.modifiedDFs["descending"]

    
    def generate(self):
        if not self.validate():
            # data and column names don't match
            # handle
            return
        
        fig = px.line(self.df, x=(self.x_axis), y=(self.y_axis), title=self.title)
        fig.update_layout(xaxis_title = natural_name(self.x_axis), yaxis_title = natural_name(self.y_axis))

        return fig

    def validate(self):
        if self.x_axis not in self.df:
            if self.y_axis in self.df and len(self.df.columns) == 2:
                self.x_axis = list(self.df.columns).remove(self.y_axis) # type: ignore
                return True
            return False
        elif self.y_axis not in self.df:
            if self.x_axis in self.df and len(self.df.columns) == 2:
                self.y_axis = list(self.df.columns).remove(self.x_axis) # type: ignore
                return True
            return False
        else:
            return True


    def getModifiers(self):
        if self.dfLength > 10:
            return ("Original", "Top 10 values only", "Ascending order by y values", "Descending order by y values")
        else:
            return ("Original", "Ascending order by y values", "Descending order by y values")

    def modify(self, modifier):
        if modifier == "Original":
            self.originalData()
        elif modifier == "Top 10 values only":
            self.topn(10)
        elif modifier == "Ascending order by y values":
            self.ascending()
        elif modifier == "Descending order by y values":
            self.descending()
        else:
            self.originalData()

    def __str__(self):
        description = (f"LineChart:\n"
                       f"Title: {self.title}\n"
                       f"X-axis: {self.x_axis} (Column name used as the X axis)\n"
                       f"Y-axis: {self.y_axis} (Column name used as the Y axis)\n"
                       f"Data: {self.df}")
        return description

# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# chart = LineChart(df, "SELECT * FROM *", {"title": "title 1", "x_axis" : "lab", "y_axis" : "val"})
# fig = chart.generate()
# fig.show()