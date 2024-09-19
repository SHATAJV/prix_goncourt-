from models.member import Member


class President(Member):
    def __init__(self, name, password, id_member, role='president'):
        super().__init__(name, password, id_member, role)
        self.id_member = id_member

    def manage_selections(self, selection):
        print(f"Managing selections for tour {selection.selection_number}:")
        for book in selection.books:
            print(f" - {book.title}")

    def result(self, book_votes):
        print("Result:")
        winner = max(book_votes, key=book_votes.get)
        for book, vote_count in book_votes.items():
            print(f"{book.title}: {vote_count} votes")
        print(f"The winner is {winner.title}!")

    def __str__(self):
        return f"President: {self.name}"
