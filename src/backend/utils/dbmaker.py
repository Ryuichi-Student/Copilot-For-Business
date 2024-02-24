""" Use this to create a SQLite database from a set of CSV files. """


import sqlite3
import pandas as pd
import glob
import pandasql as ps
from datetime import datetime


def initialize_db():
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

def db_splitter():

    # Connect to SQLite database
    conn = sqlite3.connect('C://Users/RamVi/Downloads/Copilot-For-Business/databases/crm_refined.sqlite3')

    """
    name
0         completedorder
1             CRM_Events
2   completeddisposition
3          completedcard
4    LuxuryLoanPortfolio
5   CRM_Call_Center_Logs
6          completedloan
7      completeddistrict
8         completedtrans
9            CRM_Reviews
10         completedacct
11       completedclient
    
    
    """

    query = "SELECT * FROM sqlite_master WHERE type='table';"
    df = pd.read_sql_query(query, conn)

    # Example condition: Split tables into two based on their nature
    condition_1 = "SELECT * FROM df WHERE name IN ('completedorder', 'completeddisposition', 'completedcard', 'completedloan', 'completeddistrict', 'completedtrans', 'completedacct', 'completedclient')"
    condition_2 = "SELECT * FROM df WHERE name IN ('CRM_Events', 'LuxuryLoanPortfolio', 'CRM_Call_Center_Logs', 'CRM_Reviews')"

    group1 = "Orders_Group"
    group2 = "Events_Group"

    conn_orders = sqlite3.connect(f'C://Users/RamVi/Downloads/Copilot-For-Business/databases/{group1}.sqlite3')
    conn_events = sqlite3.connect(f'C://Users/RamVi/Downloads/Copilot-For-Business/databases/{group2}.sqlite3')

    # Make a new DataFrame with condition_1
    orders_group = ps.sqldf(condition_1, locals())
    orders_group.to_sql('orders_group', conn, if_exists='replace', index=False)
    # Make a new DataFrame with condition_2
    events_group = ps.sqldf(condition_2, locals())
    events_group.to_sql('events_group', conn, if_exists='replace', index=False)


    # Save to a new database
    orders_group.to_sql('orders_group', conn_orders, if_exists='replace', index=False)
    events_group.to_sql('events_group', conn_events, if_exists='replace', index=False)

    # Commit the transaction
    conn_orders.commit()
    conn_events.commit()

    # Print the new tables

    conn.close()

    # Close the connection
    conn_orders.close()
    conn_events.close()

def db_checker():

    root_dir = "C://Users/RamVi/Downloads/Copilot-For-Business/databases/"

    group1 = "Orders_Group"
    group2 = "Events_Group"

    conn_orders = sqlite3.connect(f'{root_dir}{group1}.sqlite3')

    query = "SELECT * FROM sqlite_master WHERE type='table';"
    df_orders = pd.read_sql_query(query, conn_orders)

    print(df_orders)

    conn_orders.close()

def join_dbs(databases:list[str]):

    if len(databases) == 1:
        print("One databaseeeee")
        return databases[0]

    name = datetime.now().strftime("%Y%m%d%H%M%S")
    conn = sqlite3.connect(f"uploads/tempdb{name}.sqlite3")

    for db in databases:
        conn_db = sqlite3.connect(db)
        query = "SELECT * FROM sqlite_master WHERE type='table';"
        df = pd.read_sql_query(query, conn_db)
        df.to_sql(db, conn, if_exists='append', index=False)
        conn_db.close()

    query = "SELECT * FROM sqlite_master WHERE type='table';"
    df = pd.read_sql_query(query, conn)

    print(df)

    conn.close()

    return f"uploads/tempdb{name}.sqlite3"



if __name__ == "__main__":

    db_checker()
    print("Done")



