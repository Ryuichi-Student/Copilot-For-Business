import plotly.express as px
import pandas as pd
from src.backend.visualisation.Visualisation import Visualisation

class ScatterChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)
        self.title = info['title']
        self.x_axis = info['x_axis']
        self.y_axis = info['y_axis']
        self.modifiedDFs = {"data" : data}
    
    # functions for the actioner
    @staticmethod
    def getChartName():
        return "Scatter Plot"

    @staticmethod
    def getChartDescription():
        return "This should be chosen when a scatter plot is most suitable to represent the data, for example to display the relationship between two varying variables."

    @staticmethod
    def getChartParametersForActioner():
        return {'title': '', 'x_axis': '', 'y_axis': ''}

    @staticmethod
    def getChartParameterDescription():
        return "'title' should contain a string of the most suitable title for the scatter plot. 'x_axis' should contain a string of the column name that should be used as the x axis values of the scatter plot. 'y_axis' should contain a string of the column name that should be used as the y axis values of the scatter plot."

    # sets the database to show the top n values by y axis depending on a bool
    def topn(self, n, show):
        if n == len(self.y_axis):
            self.df = self.modifiedDFs["data"]
        else:
            if n not in self.modifiedDFs:
                self.modifiedDFs[n] = self.modifiedDFs["data"].nlargest(n, self.y_axis)
            self.df = self.modifiedDFs[n]

    def generate(self):
        if not self.validate():
            print("data is invalid")
            return
        
        # plot a scatter chart
        fig = px.scatter(self.df, x=self.x_axis, y=self.y_axis, title=self.title)

        return fig

    def validate(self):
        if self.x_axis not in self.df:
            return False
        if self.y_axis not in self.df:
            return False
        else:
            return True

    def __str__(self):
        # Construct the string description
        description = (f"Scatter Plot:\n"
                       f"Title: {self.title}\n"
                       f"X-axis: {self.x_axis} (Column name used for X axis values)\n"
                       f"Y-axis: {self.y_axis} (Column name used for Y axis values)\n"
                       f"Data: {self.df}")
        return description

# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# chart = ScatterChart(df, "SELECT * FROM *", {"title": "title 1", "x_axis" : "lab", "y_axis" : "val"})
# fig = chart.generate()
# fig.show()