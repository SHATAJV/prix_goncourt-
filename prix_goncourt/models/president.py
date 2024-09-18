from models.members import Members


class President(Members):
    def __init__(self, name, password):
        super().__init__(name, password)

    def manage_selections(self, selection_number, selection):

        print(f"Managing selections for tour {selection_number}:")
        for book in selection.books:
            print(f" - {book.title}")

    def result(self, book_votes):
            print("result:")
            winner = max(book_votes, key=book_votes.get)
            for book, vote_count in book_votes.items():
                print(f"{book}: has {vote_count} votes")
            print(f"The winner is {winner}!")



