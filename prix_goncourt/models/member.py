# models/member.py

class Member:
    """
    Represents a member of the system, which can be a public user, jury member, or president.

    Attributes:
        name (str): The name of the member.
        password (str): The password for the member's account.
        id_member (int): The unique identifier for the member.
        role (str): The role of the member (e.g., 'public', 'jury', 'president').
    """

    def __init__(self, name, password, id_member, role='public'):
        """
        Initializes a Member instance.

        Args:
            name (str): The name of the member.
            password (str): The password for the member's account.
            id_member (int): The unique identifier for the member.
            role (str, optional): The role of the member. Defaults to 'public'.
        """
        self.name = name
        self.password = password
        self.id_member = id_member
        self.role = role

    def login(self, name, password):
        """
        Authenticates the member's login credentials.

        Args:
            name (str): The name provided during login.
            password (str): The password provided during login.

        Returns:
            bool: True if the login is successful, False otherwise.
        """
        if self.name == name and self.password == password:
            print(f"Login successful! Welcome, {self.name}")
            return True
        else:
            print("Login failed!")
            return False

    def __str__(self):
        """
        Returns a string representation of the member.

        Returns:
            str: A description of the member including their name.
        """
        return f"Member: {self.name}"
