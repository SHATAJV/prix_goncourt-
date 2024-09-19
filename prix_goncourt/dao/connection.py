# dao/connection.py
import pymysql.cursors
from pymysql import MySQLError


def get_db_connection():
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
