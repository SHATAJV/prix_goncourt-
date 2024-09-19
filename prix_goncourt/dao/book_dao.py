from dao.connection import get_db_connection
import pymysql

class BookDAO:
    def get_books_by_selection(self, selection_number):
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT b.id_book, b.title, b.summary, a.name AS author, b.editor, b.publication_date, b.pages, b.isbn, b.price 
            FROM books b
            JOIN authors a ON b.id_author = a.id_author
            JOIN selections s ON b.id_book = s.id_book
            WHERE s.selection_number = %s
        """
        cursor.execute(query, (selection_number,))
        books = cursor.fetchall()
        cursor.close()
        connection.close()
        return books

    def add_books_to_selection(self, selection_number, book_ids):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO selections (selection_number, id_book) VALUES (%s, %s)"
        for book_id in book_ids:
            cursor.execute(query, (selection_number, book_id))
        connection.commit()
        cursor.close()
        connection.close()

    def get_vote_results_for_president(self, selection_number):
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT b.id_book, b.title, a.name AS author, COALESCE(SUM(v.votes_count), 0) AS votes_count
            FROM books b
            JOIN authors a ON b.id_author = a.id_author
            LEFT JOIN votes v ON b.id_book = v.id_book
            JOIN selections s ON b.id_book = s.id_book
            WHERE s.selection_number = %s
            GROUP BY b.id_book
            ORDER BY votes_count DESC
        """
        cursor.execute(query, (selection_number,))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def add_vote(self, book_id, jury_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Vérifier si un vote existe déjà pour ce livre et ce membre du jury
        check_query = """
            SELECT id_vote, votes_count FROM votes WHERE id_book = %s AND id_jury = %s
        """
        cursor.execute(check_query, (book_id, jury_id))
        result = cursor.fetchone()

        if result:
            # Si un vote existe, on incrémente votes_count
            id_vote, votes_count = result
            update_query = """
                UPDATE votes SET votes_count = %s WHERE id_vote = %s
            """
            cursor.execute(update_query, (votes_count + 1, id_vote))
        else:
            # Sinon, on insère un nouveau vote
            insert_query = """
                INSERT INTO votes (id_book, votes_count, id_jury) VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (book_id, 1, jury_id))

        connection.commit()
        cursor.close()
        connection.close()
