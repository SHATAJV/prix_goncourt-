class BookDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_books_by_selection(self, id_selection):
        cursor = self.db_connection.cursor()
        query = "SELECT title, author, publisher FROM books WHERE id_selection = %s"
        cursor.execute(query, (id_selection,))
        books = cursor.fetchall()
        cursor.close()
        return books

    def add_vote(self, book_id, jury_id):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO votes (book_id, jury_id) VALUES (%s, %s)"
        cursor.execute(query, (book_id, jury_id))
        self.db_connection.commit()
        cursor.close()
