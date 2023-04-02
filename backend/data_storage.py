import mysql.connector
from mysql.connector import Error
from config import MYSQL_CONFIG


def create_connection(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None



def execute_query(connection, query, values=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return cursor
    except Error as e:
        print(f"The error '{e}' occurred")
        return None


def store_user_preferences(host, user, password, database, user_id, portfolio_setup, data_source):
    connection = create_connection(host, user, password, database)
    
    query = "INSERT INTO user_preferences (user_id, portfolio_setup, data_source) VALUES (%s, %s, %s)"
    values = (user_id, portfolio_setup, data_source)
    
    execute_query(connection, query, values)