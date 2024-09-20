# dao/connection.py

import pymysql.cursors
from pymysql import MySQLError


def get_db_connection():
    """
    Establishes a connection to the MySQL database.

    This function attempts to connect to the MySQL database using the specified
    parameters (host, user, password, database). If the connection is successful,
    it returns the connection object. If there is an error during the connection,
    it prints an error message and returns None.

    Returns:
        connection: A connection object for interacting with the database,
                    or None if the connection fails.
    """
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1234shtaj',
            database='prix_goncourt',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None
