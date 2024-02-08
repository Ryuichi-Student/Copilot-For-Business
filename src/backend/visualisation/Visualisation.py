from typing import Dict
import pandas as pd
import matplotlib
from abc import ABC, abstractmethod

class Visualisation(ABC):
    def __init__(self, title, data, query):
        self.title = title
        self.df: pd.DataFrame = data
        self.query = query
    
    @staticmethod
    @abstractmethod
    def getChartName() -> str:
        return ''

    @staticmethod
    @abstractmethod
    def getChartDescription() -> str:
        return ''

    @staticmethod
    @abstractmethod
    def getChartParametersForActioner() -> Dict[str, str]:
        return {}
    
    @staticmethod
    @abstractmethod
    def getChartParameterDescription() -> str:
        return ''
    
    # Generates the visualisation for the class. When the base class is used the title is displayed
    @abstractmethod
    def generate(self):
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def getSQLQuery(self) -> str:
        pass