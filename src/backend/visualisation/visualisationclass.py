import pandas as pd
import matplotlib.pyplot as plt


class Visualisation:
    def __init__(self, title, data, query):
        self.title = title
        self.df = data
        self.query = query
    
    # Generates the visualisation for the class. When the base class is used the title is displayed
    def generate(self):
        print(self.title)

    # add a validate data function
    # 

    

class PieChart(Visualisation):
    def __init__(self, title, data, query, categories, percentages):
        super().__init__(title, data, query)
        self.categories = categories
        self.percentages = percentages







# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# df.plot(kind='line')
# plt.show()