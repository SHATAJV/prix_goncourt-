# -*- coding: utf-8 -*-


class Book:
    def __init__(self, title, author, editor, summary, isbn, publication_date, pages, price):
        self.title = title
        self.author = author
        self.editor = editor
        self.summary = summary
        self.isbn = isbn
        self.publication_date = publication_date
        self.pages = pages
        self.price = price
def __str__(self):
    return f"this book {self.title} was wriiten by {self.author} on {self.publication_date}"