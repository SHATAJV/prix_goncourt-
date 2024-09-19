
from dao.book_dao import BookDAO


def get_votes_from_jury(jury, selection_number):
    # Implémentez la logique pour obtenir les votes du jury, par exemple, via une entrée utilisateur ou une autre source
    return [1, 3, 8]  # Exemple de retour de fonction avec IDs des livres

def handle_selection_process(book_dao, jury_list):
    # Phase 1 : Ajout initial des livres à la sélection 1
    initial_books = [...]  # IDs des livres pour la sélection initiale
    book_dao.add_books_to_selection(1, initial_books, None)  # Pas de limitation de votes pour la sélection initiale

    # Phase 2 : Vote des jurys pour la sélection 2
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 2)  # Supposer une fonction pour obtenir les votes du jury
        book_dao.add_vote(book_ids, jury.id_member, 2)

    # Phase 3 : Président sélectionne des livres basés sur les votes
    top_books = book_dao.president_select_books(2, 8)
    book_dao.add_books_to_selection(3, [book['id_book'] for book in top_books], 2)

    # Phase 4 : Vote des jurys pour la sélection 3
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 3)
        book_dao.add_vote(book_ids, jury.id_member, 3)

    # Phase 5 : Président sélectionne le gagnant
    final_books = book_dao.president_select_books(3, 1)
    print(f"Le gagnant final est le livre avec ID: {final_books[0]['id_book']}")
