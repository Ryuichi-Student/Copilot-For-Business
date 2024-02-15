import matplotlib.pyplot as plot
import pandas as pd
import plotly.express as px
from src.backend.visualisation.Visualisation import Visualisation


class BarChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)
        self.title = info['title']
        self.x_axis = info['x_axis']
        self.y_axis = info['y_axis']
    
    # functions for the actioner
    @staticmethod
    def getChartName():
        return "Bar Chart"

    @staticmethod
    def getChartDescription():
        return "This should be chosen when a bar chart is most suitable to represent the data."
    
    # returns a dictionary of the parameters required from the Actioner to create a BarChart object
    @staticmethod
    def getChartParametersForActioner():
        return {'title': '', 'x_axis': '', 'y_axis': ''}
    
    @staticmethod
    def getChartParameterDescription():
        return "'title' should contain a string of most suitable title for the bar chart. 'x_axis' should contain a string of the column name that should be used as the x axis of the bar chart. 'y_axis' should contain a string of the column name that should be used as the y axis of the bar chart."
    
    # generates a bar chart from the data frame with the x axis and y axis provided as identifiers for the data frame
    def generate(self):
        if not self.validate():
            # return an error
            print("invalid data")
            return
        
        # x and y axis variables
        # x_axis = self.df[self.x_axis]
        # y_axis = self.df[self.y_axis]



        fig = px.bar(self.df, x=self.x_axis, y=self.y_axis, title=self.title)


        # sets the size of the bar graph
        # fig = plot.figure(figsize=(10,6))

        # # plots a bar graph
        # plot.bar(x_axis, y_axis)
        # # sets the title of the graph
        # plot.title(self.title)
        # # sets the x and y axis labels
        # # TODO: change these to natural language/remove - they're just the column names at the moment
        # plot.xlabel(self.x_axis)
        # plot.ylabel(self.y_axis)

        return fig
    
    # test for this that gives an invalid data frame
    def validate(self):
        if self.x_axis not in self.df:
            # no x axis in the data frame
            # make this better raise an error? call to gpt?
            return False
        elif self.y_axis not in self.df:
            # no yaxis in the data frame
            # raise an error
            return False
        else:
            return True
    
    



# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# bar = BarChart(df, "query", {'title': 'title1', 'x_axis': 'lab', 'y_axis': 'val'})
# fig = bar.generate()

# fig.show()