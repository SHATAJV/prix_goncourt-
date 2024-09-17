# -*- coding: utf-8 -*-
# Class Jury
from models.members import Members


class Jury(Members):
    def __init__(self, name,  password, vote_count=0):
        super().__init__(name, password)
        self.vote_count = vote_count

    def vote(self, book_title):
        self.vote_count += 1
        print(f"{self.name} voted for {book_title}")

