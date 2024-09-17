def __init__(self, book_dao):
    self.book_dao = book_dao


def display_books(self, selection_stage):
    books = self.book_dao.get_books_by_selection(selection_stage)
    print(f"Books in selection {selection_stage}:")
    for book in books:
        print(f"- {book[0]} by {book[1]}, Publisher: {book[2]}")


def vote_for_book(self, book_id, jury_id):
    self.book_dao.add_vote(book_id, jury_id)
    print("Vote recorded successfully.")
