import pymysql
from dao.connection import get_db_connection

class MembersDAO:
    def __init__(self):
        # Initialise la connexion à la base de données
        self.connection = get_db_connection()

    def get_member_by_name(self, name):
        with self.connection.cursor() as cursor:
            sql = "SELECT name, password, role, id_member FROM members WHERE name = %s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()  # Utilisez fetchone() pour obtenir une seule ligne



        if result:
            return {
                'name': result['name'],
                'password': result['password'],
                'role': result['role'],
                'id_member': result['id_member']
            }
        else:
            return None
