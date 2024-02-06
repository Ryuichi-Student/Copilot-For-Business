import pandas as pd
import matplotlib.pyplot as plot
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from visualisationclass import Visualisation



class BarChart(Visualisation):
    def __init__(self, title, data, query, xaxis, yaxis):
        super().__init__(title, data, query)
        self.xaxis = xaxis
        self.yaxis = yaxis
    
    # generates a bar chart from the data frame with the x axis and y axis provided as identifiers for the data frame
    def generate(self):
        x_axis = self.df[self.xaxis]
        y_axis = self.df[self.yaxis]
        # plots a bar graph
        plot.bar(x_axis, y_axis)
    
    # test for this that gives an invalid dataframe
    def validate(self):
        if self.xaxis not in self.df:
            # no x axis in the dataframe
            # make this better raise an error? call to gpt?
            return False
        elif self.yaxis not in self.df:
            # no yaxis in the dataframe
            # raise an error
            return False
        else:
            return True




# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# bar = BarChart("title 1", df, "SELECT * FROM *", "lab", "val")
# bar.generate()
# plot.show()