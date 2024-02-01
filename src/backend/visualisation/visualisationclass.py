class Visualisation:
    def __init__(self, title) -> None:
        self.title = title


class BarChart(Visualisation):
    def __init__(self, title, xaxis, yaxis):
        super().__init__(title)
        self.xaxis = xaxis
        self.yaxis = yaxis


bar = BarChart("title 1", "people", "cats")