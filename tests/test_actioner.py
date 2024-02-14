import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.actioner import Actioner
from src.backend.database import SQLiteDatabase

def test_action_valid():
    query = "Who is the most valuable customer?"
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    actioner = Actioner(db)
    requirements = actioner.get_requirements(query)
    command = actioner.get_action(requirements)
    assert command[0]['status'] == 'success'

def test_action_invalid():
    query = "Hello"
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    actioner = Actioner(db)
    requirements = actioner.get_requirements(query)
    command = actioner.get_action(requirements)
    assert command[0]['status'] == 'error'


def test_actioner_final_pass():
    query = "What are our most popular products?"
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    actioner = Actioner(db)
    command = actioner.get_final_action(query)
    assert command['status'] == 'success'

def test_actioner_final_fail():
    query = "Hello"
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    actioner = Actioner(db)
    command = actioner.get_final_action(query)
    assert command['status'] == 'error'