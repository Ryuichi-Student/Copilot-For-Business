from typing import Dict
import pandas as pd

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
    
    def getSQLQuery(self):
        # make this better
        # do an sql formatter function to explain to the user?
        description = (f'''
            This data used to create this chart was fetched using the following SQL query:
            
            {self.query}
        ''')
        return description