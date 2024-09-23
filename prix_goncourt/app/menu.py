from dao.book_dao import BookDAO
from dao.members_dao import MembersDAO
from models.jury import Jury
from models.president import President
from models.member import Member
from selection_process import add_votes_for_selection


def display_books_for_selection(self, selection_number):
    """
    Display the list of books available for a given selection phase.

    Args:
        selection_number (int): The number of the selection phase.
    """
    books = self.get_books_by_selection(selection_number)
    if books:
        print(f"Books available for selection phase {selection_number}:")
        for book in books:
            print(f"ID: {book['id_book']}, Title: {book['title']}, Author: {book['author']}")
    else:
        print(f"No books available for selection phase {selection_number}.")


def display_menu():
    """
    Display the main menu options for the application.
    """
    print("=== Main Menu ===")
    print("1. Login")
    print("2. Quit")


def handle_login(member, book_dao):
    """
    Handle the login process for different member roles.

    Args:
        member (Member): The member object representing the logged-in user.
        book_dao (BookDAO): Data access object for book-related operations.
    """
    if isinstance(member, President):
        display_president_menu(book_dao, member)
    elif isinstance(member, Jury):
        display_jury_menu(book_dao, member)
    elif member.role == 'public':
        display_member_menu(book_dao, "public")
    else:
        print("Unknown role.")


def display_member_menu(book_dao, member_role):
    """
    Display the menu options for public members.

    Args:
        book_dao (BookDAO): Data access object for book-related operations.
        member_role (str): The role of the member (should be 'public').
    """
    print(f"=== Menu {member_role.capitalize()} ===")
    print("1. Display books from a selection")
    print("2. Quit")
    choice = input("Choose an option: ")
    handle_member_choice(choice, book_dao)


def display_president_menu(book_dao, president):
    """
    Display the menu options for presidents.

    Args:
        book_dao (BookDAO): Data access object for book-related operations.
        president (President): The president object logged in.
    """
    while True:
        print(f"=== Menu President ({president.name}) ===")
        print("1. Add books to the selection")
        print("2. Display voting results")
        print("3. Quit")
        choice = input("Choose an option: ")

        if choice == '1':
            selection_number = int(input("Selection number (2, 3, 4): "))
            book_ids = input("Enter the IDs of books to add (separated by commas): ").split(',')
            book_ids = [int(book_id.strip()) for book_id in book_ids]
            book_dao.add_books_to_selection(selection_number, book_ids)
            print("Books added to the selection.")
        elif choice == '2':
            selection_number = int(input("Selection number (2, 3, 4): "))
            results = book_dao.get_vote_results_for_president(selection_number)
            for result in results:
                print(f"{result['title']} - {result['author']} - Votes: {result['votes_count']}")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")


def display_jury_menu(book_dao, member):
    """
    Display the menu options for jury members.

    Args:
        book_dao (BookDAO): Data access object for book-related operations.
        member (Jury): The jury member object logged in.
    """
    while True:
        print(f"=== Menu Jury ({member.name}) ===")
        print("1. Display books from a selection")
        print("2. Vote for a book")
        print("3. Quit")
        choice = input("Choose an option: ")

        if choice == '1':
            selection_number = int(input("Enter the selection number (1, 2, 3): "))
            display_books_for_selection(book_dao, selection_number)
        elif choice == '2':
            selection_number = int(input("Enter the selection number (2, 3, 4): "))
            available_books = book_dao.get_books_by_selection(selection_number)
            available_book_ids = [book['id_book'] for book in available_books]

            print(f"Available books for selection {selection_number}: {available_book_ids}")
            handle_vote(book_dao, member, selection_number)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


def handle_vote(book_dao, member, selection_number):
    """
    Handle the voting process for a jury member.

    Args:
        book_dao (BookDAO): Data access object for book-related operations.
        member (Jury): The jury member casting the vote.
        selection_number (int): The selection number for which voting is happening.
    """
    current_votes = book_dao.get_current_votes_for_jury(member.id_member, selection_number) or 0
    available_books = book_dao.get_books_by_selection(selection_number)
    available_book_ids = [book['id_book'] for book in available_books]

    # Set max votes based on the selection phase
    max_votes = {2: 4, 3: 2, 4: 1}.get(selection_number, 0)

    votes_remaining = max_votes - current_votes

    if votes_remaining > 0:
        print(f"You have {votes_remaining} votes remaining for this selection.")
        book_ids_input = input("Enter the IDs of the books to vote for (separated by commas): ")
        book_ids = [int(id.strip()) for id in book_ids_input.split(',')]

        # Validate book IDs
        invalid_books = [book_id for book_id in book_ids if book_id not in available_book_ids]
        if invalid_books:
            print(f"Error: The following books are not available for this selection: {invalid_books}")
        else:
            add_votes_for_selection(book_dao, member, selection_number, book_ids)
    else:
        print("You have exhausted your votes for this selection.")


def handle_member_choice(choice, book_dao):
    """
    Handle the member's choice from the member menu.

    Args:
        choice (str): The user's menu choice.
        book_dao (BookDAO): Data access object for book-related operations.
    """
    if choice == '1':
        selection_number = int(input("Enter the selection number (1, 2, 3): "))
        books = book_dao.get_books_by_selection(selection_number)
        if books:
            for book in books:
                print(f"ID: {book['id_book']}, Title: {book['title']}, Author: {book['author']}")
        else:
            print("No books available in this selection.")
    elif choice == '2':
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice.")

