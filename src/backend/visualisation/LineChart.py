import matplotlib.pyplot as plot
import pandas as pd
from src.backend.visualisation.Visualisation import Visualisation

class LineChart(Visualisation):
    def __init__(self, title, data, query, xaxis, yaxis):
        super().__init__(title, data, query)
        self.x_axis = xaxis
        self.y_axis = yaxis
    
    @staticmethod
    def getChartName():
        return "Line chart"
    
    @staticmethod
    def getChartDescription():
        return "This should be chosen when a line chart is most suitable to represent the data, for example to display continuous numerical data."

    @staticmethod
    def getChartParametersForActioner():
        return {'title': '', 'x_axis': '', 'y_axis': ''}
        
    @staticmethod
    def getChartParameterDescription():
        return "'title' should contain a string of most suitable title for the line chart. 'x_axis' should contain a string of the column name that should be used as the x axis of the line chart. 'y_axis' should contain a string of the column name that should be used as the y axis of the line chart."

    def generate(self):
        if not self.validate():
            # data and column names don't match
            # handle
            return
        
        x_axis = self.df[self.x_axis]
        y_axis = self.df[self.y_axis]

         # sets the size of the bar graph
        fig = plot.figure(figsize=(10,6))

        # plots a bar graph
        plot.plot(x_axis, y_axis)
        # sets the title of the graph
        plot.title(self.title)
        # sets the x and y axis labels
        # TODO: change these to natural language/remove - they're just the column names at the moment
        plot.xlabel(self.x_axis)
        plot.ylabel(self.y_axis)

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

