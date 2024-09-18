from dao.book_dao import BookDAO
from dao.dao import get_db_connection
from models.president import President

from dao.members_dao import MembersDAO

from models.members import Members
from models.jury import Jury
from models.president import President
from models.book import Book
from models.selection import Selection
from dao.book_dao import BookDAO
from models.author import Author


def display_menu():
    print("=== Menu Principal ===")
    print("1. Login")
    print("2. Quitter")

def handle_login(member):
    if member.role == "Member":
        display_member_menu()
    elif member.role == "Jury":
        display_jury_menu()
    elif member.role == "President":
        display_president_menu()

def display_member_menu():
    print("=== Member Menu ===")
    print("1. Afficher les résultats des votes")
    print("2. Quitter")

def display_jury_menu():
    print("=== Jury Menu ===")
    print("1. Afficher les résultats des votes")
    print("2. Voter pour des livres")
    print("3. Quitter")

def display_president_menu():
    print("=== President Menu ===")
    print("1. Afficher les livres d'une sélection")
    print("2. Ajouter des livres à une sélection")
    print("3. Afficher les résultats des votes")
    print("4. Quitter")

def handle_member_choice(choice, book_dao):
    if choice == '1':
        # Afficher les résultats des votes
        print("Affichage des résultats des votes...")
        # Placeholder for actual result display logic
    elif choice == '2':
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice.")

def handle_jury_choice(choice, book_dao, member):
    if choice == '1':
        # Afficher les résultats des votes
        print("Affichage des résultats des votes...")
        # Placeholder for actual result display logic
    elif choice == '2':
        # Voting logic
        print("Voting for books...")
        # Placeholder for actual voting logic
    elif choice == '3':
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice.")

def handle_president_choice(choice, book_dao, president):
    if choice == '1':
        selection_number = int(input("Selection number (1, 2, 3): "))
        books = book_dao.read_books_by_selection(selection_number)
        for book in books:
            print(f"Title: {book[0]}, Summary: {book[1]}, Author: {book[2]}, Editor: {book[3]}, Date: {book[4]}, Pages: {book[5]}, ISBN: {book[6]}, Price: {book[7]}")
    elif choice == '2':
        title = input("Title of the book: ")
        author_name = input("Author's name: ")
        editor = input("Editor: ")
        summary = input("Summary: ")
        isbn = input("ISBN: ")
        publication_date = input("Publication Date (YYYY-MM-DD): ")
        pages = int(input("Number of pages: "))
        price = float(input("Price: "))
        book = Book(title, Author(author_name), editor, summary, isbn, publication_date, pages, price)
        selection_number = int(input("Selection number (2 or 3): "))
        # Here you should have logic to add the book to the selection
        print(f"Book added to selection number {selection_number}.")
    elif choice == '3':
        # Afficher les résultats des votes
        print("Affichage des résultats des votes...")
        # Placeholder for actual result display logic
    elif choice == '4':
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice.")

def main():
    book_dao = BookDAO()
    members_dao = MembersDAO()

    while True:
        display_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            name = input("Enter your name: ")
            password = input("Enter your password: ")
            member_data = members_dao.get_member_by_name(name)
            if member_data and member_data[1] == password:
                member = Members(name, password, member_data[2])
                handle_login(member)
            else:
                print("Invalid login credentials.")
        elif choice == '2':
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
