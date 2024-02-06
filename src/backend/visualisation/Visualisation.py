import inspect
import pandas as pd
from abc import ABC, abstractmethod
from src.backend import visualisation

class Visualisation(ABC):
    def __init__(self, title, data, query):
        self.title = title
        self.df: pd.DataFrame = data
        self.query = query

    @staticmethod
    def getAllCharts():
        return inspect.getmembers(visualisation)
        return [BarChart, PieChart, NoChart]
    
    @staticmethod
    @abstractmethod
    def getChartName():
        pass

    @staticmethod
    @abstractmethod
    def getChartDescription():
        pass

    @staticmethod
    @abstractmethod
    def getChartParametersForActioner():
        pass

    @staticmethod
    @abstractmethod
    def getChartParameterDescription():
        pass
    
    # Generates the visualisation for the class. When the base class is used the title is displayed
    @abstractmethod
    def generate(self):
        pass
    
    @abstractmethod
    def validate(self):
        pass


    # add a validate data function
    # 







# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})
# df.plot(kind='line')
# plt.show()