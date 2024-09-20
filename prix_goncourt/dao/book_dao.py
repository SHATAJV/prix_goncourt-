from dao.connection import get_db_connection
import pymysql
import pymysql.cursors


class BookDAO:

    def get_books_by_selection(self, selection_number):
        """
        Fetch books available for a specific selection based on selection number.
        """
        if selection_number == 1:
            return self.fetch_all_books()
        elif selection_number in [2, 3]:
            return self.fetch_books_for_selection(selection_number - 1)
        elif selection_number == 4:
            return self.fetch_winner_for_selection(3)
        else:
            return []

    def fetch_all_books(self):
        """Fetch all books from the database."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT b.id_book, b.title, a.name AS author 
            FROM books b 
            JOIN authors a ON b.id_author = a.id_author
        """
        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()
        connection.close()
        return books

    def fetch_books_for_selection(self, selection_number):
        """Fetch books linked to a specific selection."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT b.id_book, b.title, a.name AS author
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

    def fetch_winner_for_selection(self, selection_number):
        """Fetch the winning book from a specific selection."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT b.id_book, b.title, a.name AS author
            FROM books b
            JOIN authors a ON b.id_author = a.id_author
            JOIN selections s ON b.id_book = s.id_book
            WHERE s.selection_number = %s
            LIMIT 1
        """
        cursor.execute(query, (selection_number,))
        winner = cursor.fetchone()
        cursor.close()
        connection.close()
        return winner

    def get_max_votes_for_selection(self, selection_number):
        """Retrieve the maximum number of votes allowed for a specific selection."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT max_votes FROM selections WHERE selection_number = %s"
        cursor.execute(query, (selection_number,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result['max_votes'] if result else 0

    def get_current_votes(self, selection_number, book_id):
        """Get the current vote count for a specific book in a selection."""
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT votes_count FROM votes WHERE selection_number = %s AND id_book = %s"
        cursor.execute(query, (selection_number, book_id))
        current_votes = cursor.fetchone()
        cursor.close()
        connection.close()
        return current_votes[0] if current_votes else 0

    def get_current_votes_for_jury(self, jury_id, selection_number):
        """Count the current votes for a jury member in a specific selection."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT COUNT(*) AS votes_count 
            FROM votes 
            WHERE id_jury = %s AND id_book IN (
                SELECT id_book FROM selections WHERE selection_number = %s
            )
        """
        cursor.execute(query, (jury_id, selection_number))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result['votes_count'] if result else 0

    def add_books_to_selection(self, selection_number, book_ids, previous_selection_number):
        """Add books to a specific selection, clearing previous selections if needed."""
        connection = get_db_connection()
        cursor = connection.cursor()
        if previous_selection_number:
            clear_query = "DELETE FROM selections WHERE selection_number = %s"
            cursor.execute(clear_query, (previous_selection_number,))

        for book_id in book_ids:
            query = "INSERT INTO selections (selection_number, id_book) VALUES (%s, %s)"
            cursor.execute(query, (selection_number, book_id))

        connection.commit()
        cursor.close()
        connection.close()

    def get_vote_results_for_president(self, selection_number):
        """Retrieve the vote results for a specific selection."""
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

    def add_vote(self, book_ids, jury_id, selection_number):
        """Add a vote for specified books by a jury member for a particular selection."""
        connection = get_db_connection()
        cursor = connection.cursor()
        max_votes = self.get_max_votes_for_selection(selection_number)
        current_votes = self.get_current_votes_for_jury(jury_id, selection_number)
        votes_remaining = max_votes - current_votes

        if votes_remaining <= 0:
            print("You have reached the maximum number of votes for this selection.")
            cursor.close()
            connection.close()
            return

        available_book_ids = [book['id_book'] for book in self.get_books_by_selection(selection_number)]
        invalid_books = [book_id for book_id in book_ids if book_id not in available_book_ids]
        if invalid_books:
            print(f"Error: The following books are not available for this selection: {invalid_books}")
            cursor.close()
            connection.close()
            return

        for book_id in book_ids:
            current_votes = self.get_current_votes(selection_number, book_id)
            if current_votes >= max_votes:
                print(f"No votes remaining for book ID {book_id}.")
                continue

            check_existing_vote_query = """
                SELECT id_vote, votes_count FROM votes WHERE id_book = %s AND id_jury = %s
            """
            cursor.execute(check_existing_vote_query, (book_id, jury_id))
            result = cursor.fetchone()

            if result:
                id_vote, votes_count = result
                update_query = "UPDATE votes SET votes_count = %s WHERE id_vote = %s"
                cursor.execute(update_query, (votes_count + 1, id_vote))
            else:
                insert_query = """
                    INSERT INTO votes (id_book, votes_count, id_jury, selection_number) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (book_id, 1, jury_id, selection_number))

        connection.commit()
        cursor.close()
        connection.close()

    def president_select_books(self, selection_number, num_books):
        """Select the top books based on the vote results for a specific selection."""
        results = self.get_vote_results_for_president(selection_number)
        top_books = results[:num_books]
        return top_books

    def get_jury_votes(self, jury_id):
        """Retrieve the total number of votes cast by a specific jury member."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT COUNT(*) AS vote_count FROM votes WHERE id_jury = %s"
        cursor.execute(query, (jury_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result['vote_count'] if result else None

    def get_book_by_id(self, book_id):
        """Fetch a book's details by its ID."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT id_book, title, summary, main_character, id_author, editor, publication_date, pages, isbn 
            FROM books WHERE id_book = %s
        """
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result if result else None

def display_books_for_selection(self, selection_number):
        """
        Display the list of books available for a given selection phase.
        """
        books = self.get_books_by_selection(selection_number)
        if books:
            print(f"Books available for selection phase {selection_number}:")
            for book in books:
                print(f"ID: {book['id_book']}, Title: {book['title']}, Author: {book['author']}")
        else:
            print(f"No books available for selection phase {selection_number}.")
