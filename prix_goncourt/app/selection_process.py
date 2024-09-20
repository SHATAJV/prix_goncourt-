from dao import BookDAO


def get_votes_from_jury(jury, selection_number):
    """
    Récupérer les votes d'un membre du jury pour une sélection spécifique.
    """
    print(f"Jury {jury.name}, sélection {selection_number}.")
    book_ids_input = input("Entrez les ID des livres pour voter (séparés par des virgules): ")
    book_ids = [int(book_id.strip()) for book_id in book_ids_input.split(',')]
    return book_ids


def add_votes_for_selection(book_dao, member, selection_number, book_ids):
    total_votes = 0
    valid_book_ids = []

    available_books = book_dao.get_books_by_selection(selection_number)
    available_book_ids = {book['id_book'] for book in available_books}

    for book_id in book_ids:
        if book_id in available_book_ids:
            valid_book_ids.append(book_id)
            current_votes = book_dao.get_current_votes(selection_number, book_id)
            print(f"Votes for book {book_id}: {current_votes}")  # Log des votes actuels
            total_votes += current_votes

            # Ajoutez le vote dans la base de données
            book_dao.add_vote(selection_number, book_id, member)
        else:
            print(f"Book ID {book_id} is not valid for selection {selection_number}.")

    print(f"Total votes counted for valid books: {total_votes}")

def handle_selection_process(book_dao, jury_list):
    initial_books = list(range(1, 17))  # IDs pour 16 livres
    print("Phase 1: Liste de livres préselectionnés par le président.")
    book_dao.add_books_to_selection(1, initial_books, None)

    print("Phase 2: Vote du jury pour jusqu'à 4 livres.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 1)
        add_votes_for_selection(book_dao, jury, 1, book_ids)

    print("Le président sélectionne 8 livres avec le plus de votes de la phase 2.")
    # Implémentez la sélection par le président ici...

    print("Phase 3: Vote du jury pour jusqu'à 2 livres.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 2)
        add_votes_for_selection(book_dao, jury, 2, book_ids)

    print("Le président sélectionne les meilleurs livres de la phase 3 en fonction des votes.")
    # Implémentez la sélection par le président ici...

    print("Phase 4: Vote du jury pour 1 livre de la sélection finale.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 3)
        add_votes_for_selection(book_dao, jury, 3, book_ids)

    print("Le président sélectionne le gagnant final.")
