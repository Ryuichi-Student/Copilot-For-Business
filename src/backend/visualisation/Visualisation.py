from typing import Dict
import pandas as pd
import matplotlib
from abc import ABC, abstractmethod

class Visualisation():
    def __init__(self, data, query, info):
        self.df: pd.DataFrame = data
        self.query = query
    
    @staticmethod
    def getChartName() -> str:
        return ''

    @staticmethod
    def getChartDescription() -> str:
        return ''

    @staticmethod
    def getChartParametersForActioner() -> Dict[str, str]:
        return {}
    
    @staticmethod
    def getChartParameterDescription() -> str:
        return ''
    
    # Generates the visualisation for the class. When the base class is used the title is displayed
    def generate(self):
        pass
    
    def validate(self) -> bool:
        return True
    
    def getSQLQuery(self) -> str:
        return self.query

    