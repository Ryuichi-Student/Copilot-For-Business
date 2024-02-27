""" Use this to create a SQLite database from a set of CSV files. """

import streamlit as st
import sqlite3
import pandas as pd
import glob
import pandasql as ps
from datetime import datetime
import os


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

    conn.close()

    # Close the connection
    conn_orders.close()
    conn_events.close()



def join_dbs(databases:list[str]):

    list_of_embedded_databases = []
    list_of_not_embedded_databases = []


    # Check for embeddings
    for db in databases:
        
        target_name = db + ".json"

        if os.path.exists(target_name):
            list_of_embedded_databases.append(target_name)    
        else:
            list_of_not_embedded_databases.append(target_name)

    print(list_of_embedded_databases)
    print(list_of_not_embedded_databases)



    if len(databases) == 1:
        return databases[0]

    name = datetime.now().strftime("%Y%m%d%H%M%S")
    conn = sqlite3.connect(f"uploads/tempdb{name}.sqlite3")
    cursor = conn.cursor()

    foreign_keys = {}
    primary_keys = {}

    for db in databases:
        alias = db.replace(".sqlite3", "").replace(".db", "").split("/")[-1].split("\\")[-1]
        cursor.execute(f"ATTACH DATABASE '{db}' AS {alias}")

        # Get the foreign keys for each table
        for table in cursor.execute(f"SELECT name FROM {alias}.sqlite_master WHERE type='table';").fetchall():
            table_name = table[0]
            cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            fkeys = cursor.fetchall()
            foreign_keys[table_name] = fkeys

            cursor.execute(f"PRAGMA table_info({table_name})")
            pkeys = cursor.fetchall()
            primary_keys[table_name] = pkeys



    cursor.execute("PRAGMA database_list")
    databases_t = cursor.fetchall()
    for db in databases_t:
        cursor.execute(f"SELECT name FROM {db[1]}.sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Iterate through each table and create it in the main database
        for table in tables:
            table_name = table[0]
            
            create_sql = f"CREATE TABLE {table_name} AS SELECT * FROM {table_name}"
            cursor.execute(create_sql)
            cursor.execute("PRAGMA foreign_keys = ON")


        for table_name in tables:
            table_name = table_name[0]


            cursor.execute("PRAGMA foreign_keys = ON")
            names = [p[1] for p in primary_keys[table_name]]
            types = [p[2] for p in primary_keys[table_name]]
            inner = f"{', '.join([f'{names[i]} {types[i]}' for i in range(len(names))])}"

            for fkey in foreign_keys[table_name]:
                from_col = fkey[3]
                to_table = fkey[2]
                to_col = fkey[4]


                create_sql = f"""
    CREATE TABLE temp_table ( {inner},  FOREIGN KEY ({from_col}) REFERENCES {to_table}({to_col}));
    """
            
            
                cursor.execute(create_sql)
                cursor.execute(f"PRAGMA foreign_keys = OFF")
                cursor.execute(f"INSERT INTO temp_table SELECT * FROM {table_name};")
                cursor.execute(f"PRAGMA foreign_keys = ON")


                # Check the foreign keys
                cursor.execute('PRAGMA foreign_key_list(temp_table);')

                # Delete old table and replace with new one
                cursor.execute(f"DROP TABLE {table_name};")
                cursor.execute(f"ALTER TABLE temp_table RENAME TO {table_name};")



    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return {"name": f"uploads/tempdb{name}.sqlite3", "embedded": list_of_embedded_databases, "not-embedded": list_of_embedded_databases }


@st.cache_data
def get_database_list():
    list_of_databases = glob.glob("databases/*.sqlite3")
    list_of_databases.extend(glob.glob("databases/*.db"))

    list_of_databases.extend(glob.glob("uploads/*.sqlite3"))
    list_of_databases.extend(glob.glob("uploads/*.db"))

    # Remove all databases starting with temp
    list_of_databases = [db for db in list_of_databases if "temp" not in db]

    return list_of_databases


if __name__ == "__main__":
    
    join_dbs(["databases/crm_refined.sqlite3", "databases/Orders_Group.sqlite3"])



