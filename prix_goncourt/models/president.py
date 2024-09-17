from models.members import Members


class President(Members):
    def __init__(self, name, password):
        super().__init__(name, password)

    def manage_selections(self, id_selection, books):

        print(f"Managing selections for stage {id_selection}:")
        for book in books:
            print(f" - {book}")

    def result(self, book_votes):
            print("result:")
            winner = max(book_votes, key=book_votes.get)
            for book, votes in book_votes.items():
                print(f"{book}: {votes} votes")
            print(f"The winner is {winner}!")



