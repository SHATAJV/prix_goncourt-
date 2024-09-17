# -*- coding: utf-8 -*-



# Class Members (Parent class)
class Members:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def login(self, name, password):
        if self.name == name and self.password == password:
            print(f"Login successful! Welcome, {self.name}")
            return True
        else:
            print("Login failed!")
            return False
    def role (self, role):
        ...
