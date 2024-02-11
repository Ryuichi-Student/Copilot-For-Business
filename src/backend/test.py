from src.backend.utils.database import SQLiteDatabase
from src.backend.utils.gpt import get_gpt_response
from src.backend.actioner import Actioner
import sqlite3 as sql
import pandas as pd

def dummy_test():
    return "Backend is operational"

def test_api(message_placeholder, prompt = "What is the capital of Japan?"):
    return get_gpt_response(
        ("system", "You are a helpful assistant"),
        ("user", prompt),
        stream=True,
        message_placeholder=message_placeholder
    )

def test_actioner_workflow(query):
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    actioner = Actioner(db)
    requirements = actioner.get_requirements(query)
    print(requirements)
    command = actioner.get_action(requirements[0], query)

    return command


