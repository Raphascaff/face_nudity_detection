import mysql.connector
from dotenv import dotenv_values

def connect_database():
    """
    Connect to your database using a properly setup .env file.
    """
    database_var = dotenv_values()
    try:
        mydb = mysql.connector.connect(
            host=database_var['host'],
            user=database_var['username'],
            password=database_var['password'],
            database=database_var['database']
        )
        return mydb, mydb.cursor()
    except mysql.connector.Error as err:
        raise SystemError(f"Error: {err}")

def execut_query(query: str):
    connection, cursor = connect_database()
    try:
        cursor.execute(query)
        myresult = cursor.fetchone()
        return myresult[0] if myresult else None
    finally:
        cursor.close()
        connection.close()