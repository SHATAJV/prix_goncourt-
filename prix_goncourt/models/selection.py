# -*- coding: utf-8 -*-
from models.book import Book


class Selection:
     def __init__(self, selection_number):
         self.selection_number= selection_number
         self.books = []
     def add_book (self, book):
         self.books.append(book)
     def display_book(self):
         print(f"this is selection number{self.selection_number}")
         for book in self.books:
          print(f"list of books{book.title}")

