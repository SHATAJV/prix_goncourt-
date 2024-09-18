# -*- coding: utf-8 -*-
from dao.dao import get_db_connection


class BookDAO:

    def read_book_selected(selection_number):
        connection= get_db_connection()
        cursor = connection.cursor()
        query = "SELECT b.title, b.summary, a.name, b.editor, b.publication_date, b.pages, b.isbn, b.price FROM books b JOIN JOIN authors a ON b.id_author = a.id_author WHERE s.selection_number = %s"
        cursor.execute(query, (selection_number))
        books = cursor.fetchall()
        cursor.close()
        return books

    def add_vote(id_book, id_jury):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO votes (id_book, id_jury) VALUES (%s, %s)"
        cursor.execute(query, (id_book, id_jury))
        connection.commit()
        cursor.close()
