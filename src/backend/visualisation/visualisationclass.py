import pandas as pd
import matplotlib.pyplot as plt


class Visualisation:
    def __init__(self, title, data, query):
        self.title = title
        self.df: pd.DataFrame = data
        self.query = query
    
    # Generates the visualisation for the class. When the base class is used the title is displayed
    def generate(self):
        print(self.title)
    
    def validate(self):
        return not self.df.empty

    # add a validate data function
    # 







# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# df.plot(kind='line')
# plt.show()