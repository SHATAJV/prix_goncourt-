# dao/members_dao.py
from dao.connection import get_db_connection

class MembersDAO:
    @staticmethod
    def get_member_by_name(name):
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return None
        cursor = connection.cursor()
        query = "SELECT name, password, role FROM members WHERE name = %s"
        cursor.execute(query, (name,))
        member = cursor.fetchone()
        cursor.close()
        connection.close()
        return member
