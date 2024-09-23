from dao import BookDAO


def get_votes_from_jury(jury, selection_number):
    """
    Retrieve the votes from a jury member for a specific selection.

    Args:
        jury (Jury): The jury member casting the votes.
        selection_number (int): The selection phase number.

    Returns:
        list: A list of book IDs that the jury member voted for.
    """
    print(f"Jury {jury.name}, selection {selection_number}.")
    book_ids_input = input("Enter the book IDs to vote for (separated by commas): ")
    book_ids = [int(book_id.strip()) for book_id in book_ids_input.split(',')]
    return book_ids


def add_votes_for_selection(book_dao, member, selection_number, book_ids):
    """
    Add votes for the specified selection by a jury member.

    Args:
        book_dao (BookDAO): Data access object for book-related operations.
        member (Jury): The jury member casting the votes.
        selection_number (int): The selection phase number.
        book_ids (list): The list of book IDs to vote for.
    """
    total_votes = 0
    valid_book_ids = []

    # Retrieve available books for the selection phase
    available_books = book_dao.get_books_by_selection(selection_number)
    available_book_ids = {book['id_book'] for book in available_books}

    for book_id in book_ids:
        if book_id in available_book_ids:
            valid_book_ids.append(book_id)
            current_votes = book_dao.get_current_votes(selection_number, book_id)
            print(f"Votes for book {book_id}: {current_votes}")
            total_votes += current_votes

            # Add the vote to the database
            book_dao.add_vote(selection_number, book_id, member)
        else:
            print(f"Book ID {book_id} is not valid for selection {selection_number}.")

    print(f"Total votes counted for valid books: {total_votes}")


def handle_selection_process(book_dao, jury_list):
    """
    Handle the selection process for the book award.

    Args:
        book_dao (BookDAO): Data access object for book-related operations.
        jury_list (list): List of jury members participating in the selection process.
    """
    initial_books = list(range(1, 17))  # IDs for 16 books
    print("Phase 1: List of preselected books by the president.")
    book_dao.add_books_to_selection(1, initial_books, None)

    print("Phase 2: Jury votes for up to 4 books.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 1)
        add_votes_for_selection(book_dao, jury, 1, book_ids)

    print("The president selects 8 books with the most votes from phase 2.")

    print("Phase 3: Jury votes for up to 2 books.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 2)
        add_votes_for_selection(book_dao, jury, 2, book_ids)

    print("The president selects the best books from phase 3 based on the votes.")


    print("Phase 4: Jury votes for 1 book from the final selection.")
    for jury in jury_list:
        book_ids = get_votes_from_jury(jury, 3)
        add_votes_for_selection(book_dao, jury, 3, book_ids)

    print("The president selects the final winner.")
