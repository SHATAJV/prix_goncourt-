# dao/connection.py
import pymysql.cursors
from pymysql import MySQLError

def get_db_connection():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="prix_goncourt",
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except MySQLError as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None
