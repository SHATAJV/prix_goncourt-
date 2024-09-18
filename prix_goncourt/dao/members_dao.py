# members_dao.py

import pymysql.cursors
from dao import get_db_connection

class MembersDAO:
    @staticmethod
    def get_member_by_name(name):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT name,role, password FROM members WHERE name = %s"
        cursor.execute(query, (name,))
        member = cursor.fetchone()
        cursor.close()
        connection.close()
        return member
