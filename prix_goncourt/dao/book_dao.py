from dao.connection import get_db_connection
import pymysql
import pymysql.cursors


class BookDAO:
    """
    DAO class for managing books and votes.
    """

    def add_books_to_selection(self, selection_number, book_ids):
        """
        Add books to a selection without jury ID.

        Args:
            selection_number (int): The selection phase number.
            book_ids (list): A list of book IDs to add to the selection.
        """
        connection = get_db_connection()
        cursor = connection.cursor()

        for book_id in book_ids:
            # Check if the book is already in the selection to avoid duplicates
            check_query = """
                SELECT * FROM selections WHERE selection_number = %s AND id_book = %s
            """
            cursor.execute(check_query, (selection_number, book_id))
            if cursor.fetchone() is None:
                insert_query = """
                    INSERT INTO selections (selection_number, id_book)
                    VALUES (%s, %s)
                """
                cursor.execute(insert_query, (selection_number, book_id))
                connection.commit()
                print(f"Book ID {book_id} added to selection {selection_number}.")
            else:
                print(f"Book ID {book_id} is already in selection {selection_number}.")

        cursor.close()
        connection.close()

    def get_books_by_selection(self, selection_number):
        """
        Fetch books available for the current selection.
        This method returns books from the previous selection phase.

        Args:
            selection_number (int): The selection phase number.

        Returns:
            list: List of books available for the selection.
        """
        previous_selection_number = selection_number - 1

        # If the jury is voting for the first selection, there is no previous selection.
        if previous_selection_number <= 0:
            return self.fetch_all_books()

        return self.fetch_books_for_selection(previous_selection_number)

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
        """Fetch books linked to a specific selection.

        Args:
            selection_number (int): The selection phase number.

        Returns:
            list: List of books linked to the selection.
        """
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

    def get_max_votes_for_selection(self, selection_number):
        """
        Retrieve the maximum number of votes allowed for a specific selection.

        Args:
            selection_number (int): The selection phase number.

        Returns:
            int: Maximum votes allowed for the selection.
        """
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT max_votes FROM selections WHERE selection_number = %s"
        cursor.execute(query, (selection_number,))
        result = cursor.fetchone()

        # Log for debugging
        if result:
            print(f"Max votes for selection {selection_number}: {result['max_votes']}")
        else:
            print(f"No max_votes found for selection {selection_number}.")

        cursor.close()
        connection.close()
        return result['max_votes'] if result else 0

    def get_current_votes_for_jury(self, jury_id, selection_number):
        """
        Count the current votes for a jury member in a specific selection.

        Args:
            jury_id (int): The ID of the jury member.
            selection_number (int): The selection phase number.

        Returns:
            int: Number of current votes for the jury member.
        """
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

    def add_vote(self, selection_id, book_id, jury):
        """
        Add a vote for a book in a selection by a jury member.

        Args:
            selection_id (int): The selection phase number.
            book_id (int): The ID of the book being voted for.
            jury (Jury): The jury member casting the vote.
        """
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the vote already exists
        check_existing_vote_query = """
            SELECT id_vote FROM votes WHERE id_book = %s AND id_jury = %s AND selection_number = %s
        """
        cursor.execute(check_existing_vote_query, (book_id, jury.id_member, selection_id))
        result = cursor.fetchone()

        if result:
            # If the vote already exists, update the count
            update_query = "UPDATE votes SET votes_count = votes_count + 1 WHERE id_book = %s AND id_jury = %s AND selection_number = %s"
            cursor.execute(update_query, (book_id, jury.id_member, selection_id))
            print(f"Vote updated for book ID {book_id}.")
        else:
            # Otherwise, insert a new vote
            insert_query = """
                INSERT INTO votes (id_book, votes_count, id_jury, selection_number) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (book_id, 1, jury.id_member, selection_id))
            print(f"New vote added for book ID {book_id}.")

        connection.commit()
        cursor.close()
        connection.close()

    def get_vote_results_for_president(self, selection_number):
        """
        Retrieve the vote results for a specific selection.

        Args:
            selection_number (int): The selection phase number.

        Returns:
            list: Vote results for the selection.
        """
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

    def get_current_votes(self, selection_id, book_id):
        """
        Return the number of votes for a given book in a specific selection.

        Args:
            selection_id (int): The selection phase number.
            book_id (int): The ID of the book.

        Returns:
            int: Total votes for the book in the selection.
        """
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT SUM(votes_count) AS total_votes
            FROM votes 
            WHERE selection_number = %s AND id_book = %s
        """
        cursor.execute(query, (selection_id, book_id))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        # Log the SQL result for debugging
        print(f"Query result for selection {selection_id}, book {book_id}: {result}")

        # Check if result is valid before accessing the key
        if result is None or result['total_votes'] is None:
            return 0  # Return 0 if no votes are found
        return result['total_votes']

    def get_book_by_id(self, book_id):
        """
        Fetch a book's details by its ID.

        Args:
            book_id (int): The ID of the book.

        Returns:
            dict: Details of the book or None if not found.
        """
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

    def get_all_juries(self):
        """
        Fetch all jury members from the database.

        Returns:
            list: List of jury members.
        """
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT id_member, name FROM members WHERE role = 'jury'"
        cursor.execute(query)
        juries = cursor.fetchall()
        cursor.close()
        connection.close()
        return juries
