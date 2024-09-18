# -*- coding: utf-8 -*-
from models.book import Book


class Selection:
     def __init__(self, selection_number, book:Book):
         self.selection_number= selection_number
         self.book = book
     def __str__(self):
         return f"this is selection number{self.selection_number} est these are the book whitch is selected{self.book}"