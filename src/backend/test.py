# Use this if you want to test random functions
from src.backend.utils.gpt import get_gpt_response
import sqlite3 as sql
import pandas as pd

def dummy_test():
    return "Backend is operational!"

def test_api(message_placeholder, prompt = "What is the capital of Japan?"):
    return get_gpt_response(
        ("system", "You are a helpful assistant"),
        ("user", prompt),
        stream=True,
        message_placeholder=message_placeholder
    )


def test_db():
    conn = sql.connect('databases/crm1.db')
    c = conn.cursor()

    c.execute("SELECT * FROM completedacct")

    # Fetch all rows from the query result
    rows = c.fetchall()

    # Convert the result into a pandas DataFrame
    df = pd.DataFrame(rows, columns=[description[0] for description in c.description])

    # Print the DataFrame
    print(df)