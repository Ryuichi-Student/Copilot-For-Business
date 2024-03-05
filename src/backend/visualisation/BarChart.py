import sys

import numpy as np
import plotly.express as px
from plotly_resampler import FigureResampler
from src.backend.visualisation.Visualisation import Visualisation
from src.backend.utils.clean_name import natural_name


class BarChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)
        self.title = info['title']
        self.x_axis = info['x_axis']
        self.y_axis = info['y_axis']
        self.modifiedDFs = {"data": data}
        self.graphs = {}
        self.sampled_fig = {}

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
    def topn(self, n):
        if n == len(self.modifiedDFs["data"]):
            self.modifiedDFs[n] = self.df = self.modifiedDFs["data"]
        else:
            if n not in self.modifiedDFs:
                smallest = -1
                for x in self.modifiedDFs.keys():
                    if x != "data" and x > n:
                        smallest = min(smallest, x)
                if smallest != -1:
                    self.modifiedDFs[n] = self.modifiedDFs[smallest].nlargest(n, self.y_axis)
                else:
                    self.modifiedDFs[n] = self.modifiedDFs["data"].nlargest(n, self.y_axis)
            self.df = self.modifiedDFs[n]
    
    # creates a dataframe with values in ascending order
    def ascending(self):
        if "ascending" not in self.modifiedDFs:
            self.modifiedDFs["ascending"] = self.modifiedDFs["data"].sort_values(by=self.y_axis)
        
        self.df = self.modifiedDFs["ascending"]
    
    # creates a dataframe with values in descending order
    def descending(self):
        if "descending" not in self.modifiedDFs:
            self.modifiedDFs["descending"] = self.modifiedDFs["data"].sort_values(by=self.y_axis, ascending=False)
        
        self.df = self.modifiedDFs["descending"]
        
    # generates a bar chart from the data frame with the x axis and y axis provided as identifiers for the data frame
    def generate(self):
        if not self.validate():
            # return an error
            print("invalid data")
            return
        size = len(self.df)
        if size > 50000:
            print("size too large, generating a smaller bar chart")
            self.small_generate(50000)
            return
        if self.graphs.get(size, None) is None:
            fig = self.graphs[size] = px.bar(self.df, x=self.x_axis, y=self.y_axis, title=self.title, color=self.x_axis)
            fig.update_layout(xaxis_title = natural_name(self.x_axis), yaxis_title = natural_name(self.y_axis))

        # self.graphs[size] = FigureResampler(fig)
        return self.graphs[size]

        # fig.update_layout({
        #     "plot_bgcolor": "rgba(0, 0, 0, 0)",
        #     "paper_bgcolor": "rgba(0, 0, 0, 50)",
        # })
        # fig.write_image("plots/plot.jpeg")

    def small_generate(self, size=300):
        if not self.validate():
            # return an error
            print("invalid data")
            return

        if size > len(self.df):
            return

        if self.sampled_fig.get(size, None) is None:
            df_length = len(self.df)
            print(df_length, size)

            # Step 1: Sample indexes
            sampled_indexes = np.random.choice(df_length, size=size, replace=False)

            # Step 2: Sort the sampled indexes
            sampled_indexes_sorted = np.sort(sampled_indexes)

            # Step 3: Subset the DataFrame using the sorted indexes
            sampled_df = self.df.iloc[sampled_indexes_sorted]

            self.sampled_fig[size] = FigureResampler(px.bar(sampled_df, x=self.x_axis, y=self.y_axis, title=self.title,
                                            color=self.x_axis))
            self.graphs[size] = self.sampled_fig[size]
        return self.sampled_fig[size]

    # test for this that gives an invalid data fame
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

    def getSQLQuery(self) -> str:
        return self.query

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