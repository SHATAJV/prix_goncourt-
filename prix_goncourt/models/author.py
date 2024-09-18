# -*- coding: utf-8 -*-

class Author:
    def __init__(self, name, biography=None):
        self.name = name
        self.biography = biography
    def __str__(self):
        return  f"Author {self.name}"