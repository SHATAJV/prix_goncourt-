
# dao/book_dao.py
from dao.connection import get_db_connection

class BookDAO:
    @staticmethod
    def read_books_by_selection(selection_number):
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return None
        cursor = connection.cursor()
        query = """
        SELECT b.title, b.summary, a.name AS author, b.editor, b.publication_date, b.pages, b.isbn, b.price 
        FROM books b 
        JOIN authors a ON b.id_author = a.id_author 
        JOIN selections s ON b.id_selection = s.id_selection 
        WHERE s.selection_number = %s
        """
        cursor.execute(query, (selection_number,))
        books = cursor.fetchall()
        cursor.close()
        connection.close()
        return books

    @staticmethod
    def add_vote(id_book, id_jury):
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return
        cursor = connection.cursor()
        query = "INSERT INTO votes (id_book, id_jury) VALUES (%s, %s)"
        cursor.execute(query, (id_book, id_jury))
        connection.commit()
        cursor.close()
        connection.close()
