# -*- coding: utf-8 -*-


class Book:
    """
    Represents a book with various attributes such as title, author, and publication details.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        editor (str): The editor of the book.
        summary (str): A brief summary of the book.
        isbn (str): The ISBN number of the book.
        publication_date (str): The publication date of the book.
        pages (int): The number of pages in the book.
        price (float): The price of the book.
    """

    def __init__(self, title, author, editor, summary, isbn, publication_date, pages, price):
        """
        Initializes a Book instance.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            editor (str): The editor of the book.
            summary (str): A brief summary of the book.
            isbn (str): The ISBN number of the book.
            publication_date (str): The publication date of the book.
            pages (int): The number of pages in the book.
            price (float): The price of the book.
        """
        self.title = title
        self.author = author
        self.editor = editor
        self.summary = summary
        self.isbn = isbn
        self.publication_date = publication_date
        self.pages = pages
        self.price = price

    def __str__(self):
        """
        Returns a string representation of the book.

        Returns:
            str: A description of the book including its title, author, and publication date.
        """
        return f"This book '{self.title}' was written by {self.author} and published on {self.publication_date}."
