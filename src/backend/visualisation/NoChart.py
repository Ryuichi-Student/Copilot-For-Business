from src.backend.visualisation.Visualisation import Visualisation

class NoChart(Visualisation):
    def __init__(self, data, query, info):
        super().__init__(data, query, info)

    # functions for the actioner
    @staticmethod
    def getChartName():
        return "No Chart"

    @staticmethod
    def getChartDescription():
        return "This should be chosen when a graph is not suitable to display the data."

    @staticmethod
    def getChartParametersForActioner():
        return {}

    @staticmethod
    def getChartParameterDescription():
        return "graph_info should contain an empty object."

    def generate(self):
        pass

    def validate(self):
        return True

