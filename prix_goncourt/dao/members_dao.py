import pymysql
from dao.connection import get_db_connection

class MembersDAO:
    """
    Data Access Object (DAO) for interacting with the members table in the database.

    This class provides methods to retrieve member information from the database.
    """

    def __init__(self):
        """
        Initializes the MembersDAO and establishes a connection to the database.
        """
        self.connection = get_db_connection()

    def get_member_by_name(self, name):
        """
        Retrieves a member's information by their name.

        Args:
            name (str): The name of the member to search for.

        Returns:
            dict or None: A dictionary containing member details (name, password, role, id_member)
                          if a member with the specified name exists, or None if not.
        """
        with self.connection.cursor() as cursor:
            sql = "SELECT name, password, role, id_member FROM members WHERE name = %s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()  # Use fetchone() to get a single row

        if result:
            return {
                'name': result['name'],
                'password': result['password'],
                'role': result['role'],
                'id_member': result['id_member']
            }
        else:
            return None
