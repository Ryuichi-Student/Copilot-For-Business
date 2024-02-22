import plotly.express as px
import pandas as pd
from src.backend.visualisation.Visualisation import Visualisation

class ScatterChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)
        self.title = info['title']
        self.x_axis = info['x_axis']
        self.y_axis = info['y_axis']
    
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
        if not show:
            limit = self.df.nlargest(n, self.y_axis)
            self.modifiedDF = limit
        else:
            self.modifiedDF = self.df

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


# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# chart = ScatterChart(df, "SELECT * FROM *", {"title": "title 1", "x_axis" : "lab", "y_axis" : "val"})
# fig = chart.generate()
# fig.show()