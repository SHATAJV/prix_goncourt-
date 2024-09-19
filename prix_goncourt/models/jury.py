from models.member import Member

class Jury(Member):
    def __init__(self, name, password, id_member):
        super().__init__(name, password)
        self.id_member = id_member

    def vote(self, book, votes):
        if book in votes:
            votes[book] += 1
        else:
            votes[book] = 1
        self.vote_count += 1
        print(f"{self.name} voted for {book.title}")

    def __str__(self):
        return f"Jury: {self.name}"
