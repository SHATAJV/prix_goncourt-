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
        SELECT b.id_book, b.title, b.summary, a.name AS author, b.editor, b.publication_date, b.pages, b.isbn, b.price 
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

        # Vérifie si le jury a déjà voté pour ce livre
        check_query = "SELECT * FROM votes WHERE id_book = %s AND id_jury = %s"
        cursor.execute(check_query, (id_book, id_jury))
        existing_vote = cursor.fetchone()

        if existing_vote:
            print("Vous avez déjà voté pour ce livre.")
        else:
            # Insère un nouveau vote dans la table
            insert_query = "INSERT INTO votes (id_book, id_jury, votes_count) VALUES (%s, %s, 1)"
            cursor.execute(insert_query, (id_book, id_jury))
            connection.commit()
            print("Votre vote a été enregistré avec succès.")

        cursor.close()
        connection.close()
