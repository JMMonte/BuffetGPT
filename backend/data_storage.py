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

def store_portfolio_data(user_id, initial_capital, num_stocks, investment_date):
    try:
        connection = create_connection(**MYSQL_CONFIG)
        query = "INSERT INTO portfolio_data (user_id, initial_capital, num_stocks, investment_date) VALUES (%s, %s, %s, %s)"
        values = (user_id, initial_capital, num_stocks, investment_date)
        execute_query(connection, query, values)
        return True
    except Exception as e:
        print(f"The error '{e}' occurred")
        return False

def update_portfolio_data(user_id, initial_capital, num_stocks, investment_date):
    try:
        connection = create_connection(**MYSQL_CONFIG)
        query = "UPDATE portfolio_data SET initial_capital = %s, num_stocks = %s, investment_date = %s WHERE user_id = %s"
        values = (initial_capital, num_stocks, investment_date, user_id)
        execute_query(connection, query, values)
        return True
    except Exception as e:
        print(f"The error '{e}' occurred")
        return False

def delete_portfolio_data(user_id):
    try:
        connection = create_connection(**MYSQL_CONFIG)
        query = "DELETE FROM portfolio_data WHERE user_id = %s"
        values = (user_id,)
        execute_query(connection, query, values)
        return True
    except Exception as e:
        print(f"The error '{e}' occurred")
        return False

def get_portfolio_data(user_id):
    try:
        connection = create_connection(**MYSQL_CONFIG)
        query = "SELECT * FROM portfolio_data WHERE user_id = %s"
        values = (user_id,)
        cursor = execute_query(connection, query, values)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None
