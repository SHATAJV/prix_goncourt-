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
        SELECT b.id_book, b.title, a.name AS author, b.editor, b.publication_date, b.pages, b.isbn, b.price
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
    def add_vote(id_book, id_member):
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return
        cursor = connection.cursor()
        query = "INSERT INTO votes (id_book, id_member) VALUES (%s, %s)"
        cursor.execute(query, (id_book, id_member))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_vote_results_for_president(selection_number):
        connection = get_db_connection()
        if connection is None:
            print("Failed to connect to the database.")
            return None
        cursor = connection.cursor()
        query = """
        SELECT b.title, a.name AS author, COUNT(v.id_vote) AS votes_count
        FROM books b
        JOIN authors a ON b.id_author = a.id_author
        JOIN selections s ON b.id_selection = s.id_selection
        LEFT JOIN votes v ON b.id_book = v.id_book
        WHERE s.selection_number = %s
        GROUP BY b.id_book
        """
        cursor.execute(query, (selection_number,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
