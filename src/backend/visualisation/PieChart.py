import pandas as pd
import matplotlib.pyplot as plot
import plotly.express as px

from src.backend.visualisation.Visualisation import Visualisation

class PieChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)
        self.title = info['title']
        self.categories = info['categories']
        self.count = info['count']
        self.modifiedDFs = {"data" : data}

    # functions for the actioner
    @staticmethod
    def getChartName():
        return "Pie Chart"

    @staticmethod
    def getChartDescription():
        return "This should be chosen when a pie chart is most suitable to represent the data, for example to compare parts of a whole and percentages."

    @staticmethod
    def getChartParametersForActioner():
        return {'title': '', 'categories': '', 'count': ''}

    @staticmethod
    def getChartParameterDescription():
        return "'title' should contain a string of the most suitable title for the pie chart. 'categories' should contain a string of the column name that should be used as the segment labels of the pie chart. 'count' should contain a string of the column name that should be used as the total count of occurrences of each of the segments of the pie chart."

    # sets the database to show the top n values by y axis depending on a bool
    def topn(self, n):
        if n == self.count:
            self.df = self.modifiedDFs["data"]
        else:
            if n not in self.modifiedDFs:
                self.modifiedDFs[n] = self.modifiedDFs["data"].nlargest(n, self.count)
            self.df = self.modifiedDFs[n]

    def generate(self):
        if not self.validate():
            # handle this
            print("data invalid")
            return


        fig = px.pie(self.df, names=self.categories, values=self.count, title=self.title)
        
        # gets the segment and count data from the dataframe
        # segments = self.df[self.categories]
        # percentages = self.df[self.count]

        # # set size of the figure
        # fig = plot.figure(figsize=(4,4))

        # # plot a pie chart
        # plot.pie(percentages, labels=segments)
        # # set the title
        # plot.title(self.title)

        return fig

    def validate(self):
        if self.categories not in self.df:
            # handle
            return False
        elif self.count not in self.df:
            # handle
            return False
        else:
            # both categories and and the count are in the dataframe
            return True
    
    def __str__(self):
        # Construct the string description
        description = (f"PieChart:\n"
                       f"Title: {self.title}\n"
                       f"Categories: {self.categories} (Column used for segment labels)\n"
                       f"Count: {self.count} (Column used for segment sizes)\n"
                       f"Data: {self.df}")
        return description

# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# chart = PieChart(df, "SELECT * FROM *", {"title": "title 1", "categories" : "lab", "count" : "val"})
# fig = chart.generate()
# fig.show()