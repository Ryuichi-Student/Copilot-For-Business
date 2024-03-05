from typing import Dict, Union
import pandas as pd
import re
import streamlit as st


class Visualisation():
    def __init__(self, data, query, info):
        self.df: pd.DataFrame = data
        self.query = query
        self.dfLength = len(data.index)
        self.modifiedDFs = {"data" : data}
    
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
    @st.cache_data
    def generate(self):
        pass

    def originalData(self):
        self.df = self.modifiedDFs["data"]
    
    # limits data frame to the top 10 bars
    def topn(self, n):
        pass
    
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
    
    # def formatSQL(self, placeholder=None):
    #     # display a formatted sql query
        
    #     sql = self.query
    #     # split query by words
    #     splitByWord = re.split('\s', sql)
    #     # splitByComma = re.split(', |[A-Z]+\s', sql)
        
    #     explained = 'The data used to create this chart was fetched using the following SQL query:\n\n'
        
    #     # if a string is a command then show it orange
    #     for string in splitByWord:
    #         if string.isupper():
    #             explained += f':orange[{string}] '
    #         else:
    #             explained += string
    #             explained += " "

    #     # if there is an AS show this to the user
    #     for i, word in enumerate(splitByWord):
    #         # if there is an AS phrase
    #         if word == "AS":
    #             name = re.match('^[a-zA-Z0-9_.-]*', splitByWord[i + 1])
                
    #             columns = ""
    #             for j in range (i - 1, 0, -1):
    #                 # if there's no comma in the preceding word add it to the column
    #                 if ',' not in splitByWord[j]:
    #                     columns = splitByWord[j] + " " + columns
    #                 else:
    #                     break

    #             # columns = re.match('(.*), ^[a-zA-Z0-9_.-]*', sql)

    #             if name and columns:
    #                 explained += f'\n\nThe :blue[{name.group(0)}] values are generated from :blue[{columns}]'
    #     if placeholder is None:
    #         st.write(explained)
    #     else:
    #         placeholder.write(explained)

    def getModifiers(self):
        return ""

    def modify(self, modifier):
        pass


