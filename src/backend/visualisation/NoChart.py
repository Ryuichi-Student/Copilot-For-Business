from src.backend.visualisation.Visualisation import Visualisation

class NoChart(Visualisation):
    def __init__(self, title, data, query):
        super().__init__(title, data, query)

    # functions for the actioner
    @staticmethod
    def getChartName():
        return "No Chart"

    @staticmethod
    def getChartDescription():
        return "This should be chosen when none of the other graphs from are suitable to represent the data."

    @staticmethod
    def getChartParametersForActioner():
        return {}

    @staticmethod
    def getChartParameterDescription():
        return ""

    def generate(self):
        pass

    def validate(self):
        return True


# df = pd.DataFrame({'lab':['A', 'B', 'C'], 'val':[10, 30, 20]})

# bar = PieChart("title 1", df, "SELECT * FROM *", "lab", "val")
# bar.generate()
# plot.show()