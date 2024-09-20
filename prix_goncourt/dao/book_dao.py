from dao.connection import get_db_connection
import pymysql
import pymysql.cursors


class BookDAO:

    def get_books_by_selection(self, selection_number):
        """
        Fetch books available for the current selection based on the selection number.
        However, it fetches books from the previous selection phase.
        """
        # Si le jury vote pour la sélection 2, on veut récupérer les livres de la sélection 1.
        # De même, si c'est pour la sélection 3, on récupère les livres de la sélection 2.
        previous_selection_number = selection_number - 1

        # Si le jury vote pour la première sélection, il n'y a pas de sélection précédente.
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

    def get_max_votes_for_selection(self, selection_number):
        """Retrieve the maximum number of votes allowed for a specific selection."""
        connection = get_db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        query = "SELECT max_votes FROM selections WHERE selection_number = %s"
        cursor.execute(query, (selection_number,))
        result = cursor.fetchone()

        # Log the result for debugging
        if result:
            print(f"Max votes query result for selection {selection_number}: {result['max_votes']}")
        else:
            print(f"No max_votes found for selection {selection_number}")

        cursor.close()
        connection.close()
        return result['max_votes'] if result else 0

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

    def add_vote(self, selection_id, book_id, jury):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Vérifiez si le vote existe déjà
        check_existing_vote_query = """
            SELECT id_vote FROM votes WHERE id_book = %s AND id_jury = %s AND selection_number = %s
        """
        cursor.execute(check_existing_vote_query, (book_id, jury.id_member, selection_id))
        result = cursor.fetchone()

        if result:
            # Si le vote existe déjà, on peut mettre à jour le compteur
            update_query = "UPDATE votes SET votes_count = votes_count + 1 WHERE id_book = %s AND id_jury = %s AND selection_number = %s"
            cursor.execute(update_query, (book_id, jury.id_member, selection_id))
            print(f"Vote mis à jour pour le livre ID {book_id}.")
        else:
            # Sinon, insérer un nouveau vote
            insert_query = """
                INSERT INTO votes (id_book, votes_count, id_jury, selection_number) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (book_id, 1, jury.id_member, selection_id))
            print(f"Nouveau vote ajouté pour le livre ID {book_id}.")

        connection.commit()
        cursor.close()
        connection.close()

    def get_vote_results_for_president(self, selection_number):
        """
        Retrieve the vote results for a specific selection.
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
        """Retourne le nombre de votes pour un livre donné dans une sélection spécifique."""
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

        # Vérifiez si result est valide avant d'accéder à la clé
        if result is None or result['total_votes'] is None:
            return 0  # Retourne 0 si aucun vote n'a été trouvé
        return result['total_votes']

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



