import sys

import plotly.express as px
from plotly_resampler import FigureResampler
from src.backend.visualisation.Visualisation import Visualisation


class BarChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)
        self.title = info['title']
        self.x_axis = info['x_axis']
        self.y_axis = info['y_axis']
        self.modifiedDFs = {"data" : data}
        self.graphs = None


    # functions for the actioner
    @staticmethod
    def getChartName():
        return "Bar Chart"

    @staticmethod
    def getChartDescription():
        return "This should be chosen when a bar chart is most suitable to represent the data, for example to compare numerical data between different groups."
    
    # returns a dictionary of the parameters required from the Actioner to create a BarChart object
    @staticmethod
    def getChartParametersForActioner():
        return {'title': '', 'x_axis': '', 'y_axis': ''}
    
    @staticmethod
    def getChartParameterDescription():
        return "'title' should contain a string of most suitable title for the bar chart. 'x_axis' should contain a string of the column name that should be used as the x axis of the bar chart. 'y_axis' should contain a string of the column name that should be used as the y axis of the bar chart."
    
    # sets the database to show the top n values by y axis depending on a bool
    def topn(self, n, show):
        if "topn" not in self.modifiedDFs:
            self.modifiedDFs["topn"] = self.modifiedDFs["data"].nlargest(n, self.y_axis)
        
        if show:
            self.df = self.modifiedDFs["topn"]
        else:
            self.df = self.modifiedDFs["data"]
            

    # generates a bar chart from the data frame with the x axis and y axis provided as identifiers for the data frame
    def generate(self):
        if not self.validate():
            # return an error
            print("invalid data")
            return
        
        fig = px.bar(self.df, x=self.x_axis, y=self.y_axis, title=self.title, color=self.x_axis)
            # self.graphs["original"] = fig

        # fig.update_layout({
        #     "plot_bgcolor": "rgba(0, 0, 0, 0)",
        #     "paper_bgcolor": "rgba(0, 0, 0, 50)",
        # })
        fig.write_image("plots/plot.jpeg")
        
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
    
    def getSQLQuery(self) -> str:
        return self.query

    def __str__(self):
        
        description = (f"BarChart:\n"
                       f"Title: {self.title}\n"
                       f"X-axis: {self.x_axis} (Column name used as the X axis)\n"
                       f"Y-axis: {self.y_axis} (Column name used as the Y axis)\n"
                       f"Data: {self.df}")
        return description




# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# bar = BarChart(df, "query", {'title': 'title1', 'x_axis': 'lab', 'y_axis': 'val'})
# fig = bar.generate()

# fig.show()