import matplotlib.pyplot as plot
import pandas as pd
import plotly.express as px

# for running this file only
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from src.backend.visualisation.Visualisation import Visualisation

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
    def topn(self, n, show):
        if not show:
            limit = self.df.nlargest(n, self.y_axis)
            self.modifiedDF = limit
        else:
            self.modifiedDF = self.df

    
    def generate(self):
        if not self.validate():
            # data and column names don't match
            # handle
            return
        
        fig = px.line(self.df, x=self.x_axis, y=self.y_axis, title=self.title)
        
        # x_axis = self.df[self.x_axis]
        # y_axis = self.df[self.y_axis]

         # sets the size of the bar graph
        # fig = plot.figure(figsize=(10,6))

        # # plots a bar graph
        # plot.plot(x_axis, y_axis)
        # # sets the title of the graph
        # plot.title(self.title)
        # # sets the x and y axis labels
        # # TODO: change these to natural language/remove - they're just the data frame column names at the moment
        # plot.xlabel(self.x_axis)
        # plot.ylabel(self.y_axis)

        return fig

    def validate(self):
        if self.x_axis not in self.df:
            # handle
            return False
        elif self.y_axis not in self.df:
            # handle
            return False
        else:
            return True

# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# chart = LineChart(df, "SELECT * FROM *", {"title": "title 1", "x_axis" : "lab", "y_axis" : "val"})
# fig = chart.generate()
# fig.show()