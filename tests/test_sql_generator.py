import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test from backend
from src.backend.sql.generator import SQLGenerator

# def test_parse_query():

#     sql_generator = SQLGenerator(None, None, None, None)

<<<<<<< HEAD
    result = sql_generator.parseQuery("Mock GPT response")
=======
#     result = sql_generator._parseQuery("Mock GPT response")
>>>>>>> 6dcc286e9b5d4214c2a5215cdfb419d62d372441

#     assert isinstance(result, str)
