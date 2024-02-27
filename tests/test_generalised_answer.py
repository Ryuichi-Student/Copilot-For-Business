import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pandas import pd

from src.backend import generalised_answer

class TestGenralisedAnswer:
    def test_getAnswer_with_graph(self):
        graph_data = "Sales - January: $1000, February: $1500, March: $1200"
        prompt = "What is the trend in sales over the first quarter?"
        action_command = {"command": "fetch_sales_data", "status": "success"}
        query = "SELECT month, sales FROM sales_data WHERE month IN ('January', 'February', 'March')"
        is_graph = True
        instance = generalised_answer.general_answer_gen(graph_data, prompt, action_command, query, is_graph)
        response = instance.getAnswer()
        assert response is not None
        assert isinstance(response, str)

    def test_getAnswer_without_graph(self):
        # Create a DataFrame for non-graph data
        data = pd.DataFrame({
            'client_id': ['Client A', 'Client B', 'Client C'],
            'orders': [10, 15, 5]
        })
        prompt = "Which client placed the most orders?"
        action_command = {"command": "fetch_order_data", "status": "success"}
        query = "SELECT client_id, COUNT(order_id) as orders FROM orders GROUP BY client_id"
        is_graph = False
        instance = generalised_answer.general_answer_gen(data, prompt, action_command, query, is_graph)
        response = instance.getAnswer()
        assert response is not None
        assert isinstance(response, str)