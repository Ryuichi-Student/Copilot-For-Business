import os, sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.backend import generalised_answer

class TestGenralisedAnswer:
    def test_getAnswer_with_graph_data(self):
        graph_data = "Sales - January: $1000, February: $1500, March: $1200"
        prompt = "What is the trend in sales over the first quarter?"
        action_command = {"command": "fetch_sales_data", "status": "success"}
        query = "SELECT month, sales FROM sales_data WHERE month IN ('January', 'February', 'March')"
        is_graph = True
        instance = generalised_answer.general_answer_gen(graph_data, prompt, action_command, query, is_graph)
        response = instance.getAnswer()
        self.assertTrue(bool(response))
        self.assertIsInstance(response, str) 
