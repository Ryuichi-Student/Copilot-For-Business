import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(sys.path)

from src.backend.sql_generator.sql_generator_template import SQLGenerator

def test_parse_query():

    sql_generator = SQLGenerator(None, None, None, None)

    result = sql_generator._parseQuery("Mock GPT response")

    assert isinstance(result, str)
