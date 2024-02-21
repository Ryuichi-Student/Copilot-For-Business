""" Use this to create a SQLite database from a set of CSV files. """


import sqlite3
import pandas as pd
import glob


if __name__ == "__main__":
    # Connect to SQLite database
    conn = sqlite3.connect('../../../legacy/databases/crm1.db')

    # List all CSV files
    csv_files = glob.glob('*.csv')

    # For each CSV file
    for file in csv_files:
        # Read CSV file into DataFrame with low_memory set to False
        df = pd.read_csv(file, low_memory=False, encoding='ISO-8859-1')

        # Convert DataFrame into SQL table
        df.to_sql(file.replace('.csv', ''), conn, if_exists='replace', index=False)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()
