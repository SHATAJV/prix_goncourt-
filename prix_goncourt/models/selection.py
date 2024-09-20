class Selection:
    def __init__(self, selection_number):
        """
        Initialize a new selection with a given selection number.

        Args:
            selection_number (int): The number of the selection.
        """
        self.selection_number = selection_number
        self.books = []
        self.votes = {}

    def add_book(self, book):
        """
        Add a book to the selection.

        Args:
            book (Book): The book to add to the selection.
        """
        self.books.append(book)

    def display_books(self):
        """
        Display the books in the selection.
        """
        print(f"This is selection number {self.selection_number}:")
        for book in self.books:
            print(f" - {book.title}")

    def record_vote(self, book_id):
        """
        Record a vote for a specific book by its ID.

        Args:
            book_id (int): The ID of the book being voted for.
        """
        if book_id in self.votes:
            self.votes[book_id] += 1
        else:
            self.votes[book_id] = 1
