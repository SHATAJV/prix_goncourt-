from dao import BookDAO


def add_votes_for_selection(book_dao, jury, selection_id, book_ids):
    max_votes = 4  # Maximum de votes autorisés

    # Utilisez selection_id ici
    current_votes = sum(book_dao.get_current_votes(selection_id, book_id) for book_id in book_ids)

    if current_votes + len(book_ids) > max_votes:
        print("You have reached the maximum number of votes for this selection.")
        return

    for book_id in book_ids:
        book = book_dao.get_book_by_id(book_id)
        if book is None:
            print(f"Book with ID {book_id} does not exist.")
            continue

        book_dao.add_vote(selection_id, book_id, jury)
        print(f"Jury member {jury.name} voted for book ID {book_id} in selection {selection_id}.")



def get_votes_from_jury(jury, selection_number):
    """
    Retrieve votes from a jury member for a specific selection.

    Args:
        jury: The jury member voting.
        selection_number (int): The selection round number for which the jury is voting.

    Returns:
        list: A list of book IDs that the jury member has voted for.
    """
    print(f"Jury {jury.name}, sélection {selection_number}.")
    book_ids_input = input("Entrez les ID des livres pour voter (séparés par des virgules): ")
    book_ids = [int(book_id.strip()) for book_id in book_ids_input.split(',')]
    return book_ids

def handle_selection_process(book_dao: BookDAO, jury_list):
    """
    Manage the entire selection process, including jury voting and president selections.

    Args:
        book_dao (BookDAO): The database or service that handles book selections and votes.
        jury_list (list): A list of jury members participating in the selection process.
    """
    # Phase 1: Initial Book List (no jury voting, only president selection)
    initial_books = list(range(1, 17))  # Example IDs for 16 books
    print("Phase 1: Initial book list preselected by the president.")
    book_dao.add_books_to_selection(1, initial_books, None)

    # Phase 2: Jury voting - vote for up to 4 books
    print("Phase 2: Jury voting for up to 4 books.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 1)  # Jury votes for 4 books from selection 1
        add_votes_for_selection(book_dao, jury, 1, book_ids)

    # The president selects the top 8 books based on the vote count
    print("President selects 8 books with the most votes from Phase 2.")
    top_books = book_dao.president_select_books(1, 8)  # Select top 8 books
    book_dao.add_books_to_selection(2, [book['id_book'] for book in top_books], 1)

    # Phase 3: Jury voting - vote for up to 2 books
    print("Phase 3: Jury voting for up to 2 books from the 8 selected in Phase 2.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 2)  # Jury votes for 2 books from selection 2
        add_votes_for_selection(book_dao, jury, 2, book_ids)

    # The president selects top books (e.g., 4) based on the votes
    print("President selects top books from Phase 3 based on votes.")
    top_books = book_dao.president_select_books(2, 4)  # Select top 4 books
    book_dao.add_books_to_selection(3, [book['id_book'] for book in top_books], 2)

    # Phase 4: Jury voting - vote for 1 book
    print("Phase 4: Jury voting for 1 book from the final selection.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 3)  # Jury votes for 1 book from selection 3
        add_votes_for_selection(book_dao, jury, 3, book_ids)

    # The president selects the final winner based on the final votes
    print("President selects the final winner.")
    final_books = book_dao.president_select_books(3, 1)  # Select the final winning book
    if final_books:
        print(f"The winning book is: {final_books[0]['title']} by {final_books[0]['author']}.")
    else:
        print("No winner selected.")
