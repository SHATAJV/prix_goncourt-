from dao.connection import get_db_connection
import pymysql
import pymysql.cursors

class BookDAO:

    def get_books_by_selection(self, selection_number):
        """
        Retrieve books associated with a specific selection number.

        Args:
            selection_number (int): The selection round number.

        Returns:
            list: A list of dictionaries containing book details (ID, title, author).
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
            selection_number (int): The selection round number.

        Returns:
            int or None: The maximum number of votes, or None if the selection does not exist.
        """
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT max_votes FROM selections WHERE selection_number = %s"
        cursor.execute(query, (selection_number,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return result.get('max_votes')
        else:
            return None

    def get_current_votes_for_jury(self, jury_id, selection_number):
        """
        Count the current votes for a jury member in a specific selection.

        Args:
            jury_id (int): The ID of the jury member.
            selection_number (int): The selection round number.

        Returns:
            int: The number of votes cast by the jury member for that selection.
        """
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT COUNT(*) AS votes_count FROM votes WHERE id_jury = %s AND id_book IN (
                SELECT id_book FROM selections WHERE selection_number = %s
            )
        """
        cursor.execute(query, (jury_id, selection_number))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return result['votes_count']
        else:
            return 0

    def add_books_to_selection(self, selection_number, book_ids, previous_selection_number):
        """
        Add books to a specific selection, optionally clearing a previous selection.

        Args:
            selection_number (int): The selection round number to which books are added.
            book_ids (list): A list of book IDs to add to the selection.
            previous_selection_number (int or None): The previous selection number to clear.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO selections (selection_number, id_book) VALUES (%s, %s)"

        if previous_selection_number:
            clear_query = "DELETE FROM selections WHERE selection_number = %s"
            cursor.execute(clear_query, (previous_selection_number,))

        for book_id in book_ids:
            cursor.execute(query, (selection_number, book_id))
        connection.commit()
        cursor.close()
        connection.close()

    def get_vote_results_for_president(self, selection_number):
        """
        Retrieve the vote results for a specific selection, including book titles and authors.

        Args:
            selection_number (int): The selection round number.

        Returns:
            list: A list of dictionaries containing vote results (book ID, title, author, votes count).
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

    def add_vote(self, book_ids, jury_id, selection_number):
        """
        Add a vote for specified books by a jury member for a particular selection.

        Args:
            book_ids (list): A list of book IDs the jury member is voting for.
            jury_id (int): The ID of the jury member casting the vote.
            selection_number (int): The selection round number.
        """
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check how many votes are allowed for the selection
        max_votes = self.get_max_votes_for_selection(selection_number)
        current_votes = self.get_current_votes_for_jury(jury_id, selection_number)
        votes_remaining = max_votes - current_votes

        if votes_remaining <= 0:
            print("Vous avez atteint le nombre maximum de votes pour cette sélection.")
            cursor.close()
            connection.close()
            return

        for book_id in book_ids:
            # Check if a vote already exists for this book and jury member
            check_existing_vote_query = """
                SELECT id_vote, votes_count FROM votes WHERE id_book = %s AND id_jury = %s
            """
            cursor.execute(check_existing_vote_query, (book_id, jury_id))
            result = cursor.fetchone()

            if result:
                # If a vote exists, increment the votes_count
                id_vote, votes_count = result
                update_query = """
                    UPDATE votes SET votes_count = %s WHERE id_vote = %s
                """
                cursor.execute(update_query, (votes_count + 1, id_vote))
            else:
                # Otherwise, insert a new vote
                insert_query = """
                    INSERT INTO votes (id_book, votes_count, id_jury, selection_number) VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (book_id, 1, jury_id, selection_number))

        connection.commit()
        cursor.close()
        connection.close()

    def president_select_books(self, selection_number, num_books):
        """
        Select the top books based on the vote results for a specific selection.

        Args:
            selection_number (int): The selection round number.
            num_books (int): The number of top books to select.

        Returns:
            list: A list of dictionaries representing the top books.
        """
        results = self.get_vote_results_for_president(selection_number)
        top_books = results[:num_books]
        return top_books

    def get_jury_votes(self, jury_id):
        """
        Retrieve the total number of votes cast by a specific jury member.

        Args:
            jury_id (int): The ID of the jury member.

        Returns:
            int or None: The total vote count, or None if no votes were found.
        """
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT COUNT(*) AS vote_count
            FROM votes
            WHERE id_jury = %s
        """
        cursor.execute(query, (jury_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return result['vote_count']
        return None

