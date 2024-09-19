# models/member.py
class Member:
    def __init__(self, name, password,id_member, role= 'public'):
        self.name = name
        self.password = password
        self.id_member = id_member
        self.role = role

    def login(self, name, password):
        if self.name == name and self.password == password:
            print(f"Login successful! Welcome, {self.name}")
            return True
        else:
            print("Login failed!")
            return False

    def __str__(self):
        return f"Member: {self.name}"
