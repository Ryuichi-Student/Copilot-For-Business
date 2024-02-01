import sqlite3 as sql
import pandas as pd

def test_db():
    # conn = sql.connect('databases/crm1.db')
    # c = conn.cursor()

    # c.execute("SELECT * FROM completedacct")

    # # Fetch all rows from the query result
    # rows = c.fetchall()

    # # Convert the result into a pandas DataFrame
    # df = pd.DataFrame(rows, columns=[description[0] for description in c.description])

    # # Print the DataFrame
    # print(df)

if __name__ == "__main__":
    test_db()