# -*- coding: utf-8 -*-
from models.book import Book


class Selection:
    """
    Represents a selection round for book voting.

    Attributes:
        selection_number (int): The number of the selection round.
        books (list): A list of books included in the selection.
    """

    def __init__(self, selection_number):
        """
        Initializes a Selection instance.

        Args:
            selection_number (int): The number of the selection round.
        """
        self.selection_number = selection_number
        self.books = []

    def add_book(self, book):
        """
        Adds a book to the selection.

        Args:
            book (Book): The book to be added to the selection.
        """
        self.books.append(book)

    def display_books(self):
        """
        Displays the selection number and the list of books in the selection.
        """
        print(f"This is selection number {self.selection_number}:")
        for book in self.books:
            print(f" - {book.title}")
