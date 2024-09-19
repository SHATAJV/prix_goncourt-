from dao.connection import get_db_connection
import pymysql


class BookDAO:
    def get_books_by_selection(self, selection_number):
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
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT max_votes FROM selections WHERE selection_number = %s"
        cursor.execute(query, (selection_number,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            max_votes = result['max_votes']
        else:
            max_votes = 0
            print(f"Aucune donnée trouvée pour selection_number {selection_number}.")

        return max_votes

    def get_current_votes_for_jury(self, jury_id, selection_number):
        connection = get_db_connection()
        cursor = connection.cursor()
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
            current_votes = result['votes_count']
        else:
            current_votes = 0

        return current_votes

    def add_books_to_selection(self, selection_number, book_ids, previous_selection_number):
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO selections (selection_number, id_book) VALUES (%s, %s)"

        if previous_selection_number:
            # Clear the previous selection if specified
            clear_query = "DELETE FROM selections WHERE selection_number = %s"
            cursor.execute(clear_query, (previous_selection_number,))

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

    def add_vote(self, book_ids, jury_id, selection_number):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Vérifiez combien de votes sont autorisés pour la sélection
        max_votes = self.get_max_votes_for_selection(selection_number)

        # Vérifiez combien de votes ont déjà été effectués par ce jury pour cette sélection
        current_votes = self.get_current_votes_for_jury(jury_id, selection_number)
        votes_remaining = max_votes - current_votes

        if votes_remaining <= 0:
            print("Vous avez atteint le nombre maximum de votes pour cette sélection.")
            cursor.close()
            connection.close()
            return

        for book_id in book_ids:
            # Vérifier si un vote existe déjà pour ce livre et ce membre du jury
            check_existing_vote_query = """
                SELECT id_vote, votes_count FROM votes WHERE id_book = %s AND id_jury = %s
            """
            cursor.execute(check_existing_vote_query, (book_id, jury_id))
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
                    INSERT INTO votes (id_book, votes_count, id_jury, selection_number) VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (book_id, 1, jury_id, selection_number))

        connection.commit()
        cursor.close()
        connection.close()

    def president_select_books(self, selection_number, num_books):
        results = self.get_vote_results_for_president(selection_number)
        top_books = results[:num_books]
        return top_books
