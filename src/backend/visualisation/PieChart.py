import sys, os
import pandas as pd
import matplotlib.pyplot as plot
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from visualisationclass import Visualisation


class PieChart(Visualisation):
    def __init__(self, title, data, query, categories, count):
        super().__init__(title, data, query)
        self.categories = categories
        self.count = count

    # functions for the actioner
    @staticmethod
    def getChartName():
        return "Pie Chart"

    @staticmethod
    def getChartDescription():
        return "This should be chosen when a pie chart is most suitable to represent the data. The following values for graph_type and graph_info should be used."

    @staticmethod
    def getChartParametersForActioner():
        return {'title': '', 'categories': '', 'count': ''}

    @staticmethod
    def getChartParameterDescription():
        return "title should contain a string of the most suitable title for the pie chart. categories should contain a string of the column name that should be used as the segment labels of the pie chart. count should contain a string of the column name that should be used as the total count of occurrences of each of the segments of the pie chart."

    def generate(self):
        segments = self.df[self.categories]
        percentages = self.df[self.count]
        # plot a pie chart
        plot.pie(percentages, labels=segments)


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


# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# bar = PieChart("title 1", df, "SELECT * FROM *", "lab", "val")
# bar.generate()
# plot.show()