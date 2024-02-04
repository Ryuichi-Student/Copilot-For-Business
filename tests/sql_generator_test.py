import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test from backend
from src.backend.sql.generator import SQLGenerator

def test_parse_query():

    sql_generator = SQLGenerator(None, None, None, None)

    result = sql_generator._parseQuery("Mock GPT response")

    assert isinstance(result, str)
