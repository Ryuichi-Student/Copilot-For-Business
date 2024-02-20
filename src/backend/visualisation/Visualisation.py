from typing import Dict
import pandas as pd
import re
import streamlit as st


class Visualisation():
    def __init__(self, data, query, info):
        self.df: pd.DataFrame = data
        self.query = query
        self.dfLength = len(data.index)
    
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
    
    # limits data frame to the top 10 bars
    def topn(self, n, show):
        if not show:
            limit = self.df.nlargest(n, self.y_axis)
            self.modifiedDF = limit
        else:
            self.modifiedDF = self.df
    

    def validate(self) -> bool:
        return True
    
    def getSQLQuery(self):
        # make this better
        # do an sql formatter function to explain to the user?
        # description = (f'''
        #     The data used to create this chart was fetched using the following SQL query:
            
        #     {self.query}
        # ''')
        return self.query
    
    def formatSQL(self):
        # display a formatted sql query
        
        # split text on uppercase words
        sql = self.query
        # splits the query based on uppercase and following words
        # phrases = re.findall('[A-Z]*[^A-Z]*', sql)

        # splits the sql query by uppercase words (commands) and others
        splitByCommand = re.findall('[A-Z]*|[^A-Z]*', sql)
        
        formatted = 'The data used to create this chart was fetched using the following SQL query:\n\n'

        for string in splitByCommand:
            if string.isupper():
                formatted += f':orange[{string}]'
            else:
                formatted += string

        st.write(formatted)



