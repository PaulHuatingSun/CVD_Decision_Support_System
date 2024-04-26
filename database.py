import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database(dbname, user, host):
    # Connect to the default database
    conn = psycopg2.connect(dbname='postgres', user=user, host=host)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Set the isolation level for the connection
    cur = conn.cursor()
    
    # Create the new database
    cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(dbname)))
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
    cur.close()
    conn.close()

def run_sql_file(filename, dbname, user, host):
    # Connect to the newly created database
    conn = psycopg2.connect(dbname=dbname, user=user, host=host)
    cur = conn.cursor()

    # Open and run the SQL file
    with open(filename, 'r') as file:
        sql_script = file.read()
    cur.execute(sql_script)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    # Change the database name, user, and host if neccessary, assuming there is not password or port
    create_database(dbname = 'Test', user='dadb', host='127.0.0.1')
    
    # Change the database name, user, and host if neccessary, assuming there is not password or port
    run_sql_file('data/database.sql', dbname='Test', user='dadb', host='127.0.0.1')