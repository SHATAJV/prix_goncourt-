# models/jury.py
from models.member import Member

class Jury(Member):
    def __init__(self, name, password, vote_count=0):
        super().__init__(name, password)
        self.vote_count = vote_count

    def vote(self, book, votes):
        if book in votes:
            votes[book] += 1
        else:
            votes[book] = 1
        self.vote_count += 1
        print(f"{self.name} voted for {book.title}")

    def __str__(self):
        return f"Jury: {self.name}"
