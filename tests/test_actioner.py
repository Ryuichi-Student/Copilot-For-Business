import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.actioner import Actioner
from src.backend.utils.database import SQLiteDatabase



def test_requirements():
    actioner = Actioner(None)

    # Simple test
    requirements = actioner.get_requirements("What is the average salary of a data scientist?")
    print(requirements)
    assert len(requirements) == 1

    # Test with multiple requirements
    requirements = actioner.get_requirements("What are our most popular products?")
    print(requirements)
    assert 1 < len(requirements) == len(set(requirements))

def test_action_valid():

    query = "Who is the most valuable customer?"
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    actioner = Actioner(db)
    requirements = actioner.get_requirements(query)
    command = actioner.get_action(requirements[0], query)

    # Convert command into json
    command = json.loads(command)
    print(command)

    assert command['status'] == 'success'

def test_action_invalid():

    query = "Hello"
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    actioner = Actioner(db)
    requirements = actioner.get_requirements(query)
    command = actioner.get_action(requirements[0], query)

    # Convert command into json
    command = json.loads(command)
    print(command)

    assert command['status'] == 'error'

if __name__ == "__main__":
    test_requirements()