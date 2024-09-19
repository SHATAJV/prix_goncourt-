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

        # Afficher le résultat pour déboguer
        print(f"DEBUG: Result type: {type(result)}")
        print(f"DEBUG: Result content: {result}")

        if result:
            return {
                'name': result['name'],
                'password': result['password'],
                'role': result['role'],
                'id_member': result['id_member']  # Utilisez les noms des colonnes pour accéder aux valeurs
            }
        else:
            return None
