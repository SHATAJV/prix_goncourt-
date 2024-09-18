# app/main.py
from models.member import Member
from models.jury import Jury
from models.president import President
from dao.book_dao import BookDAO
from dao.members_dao import MembersDAO

def display_menu():
    print("=== Menu Principal ===")
    print("1. Login")
    print("2. Quitter")

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

def handle_member_choice(choice):
    if choice == '1':
        print("Affichage des résultats des votes...")
        # Placeholder for actual result display logic
    elif choice == '2':
        print("Goodbye!")
        exit()
    else:
        print("Invalid choice.")

def handle_jury_choice(choice, book_dao, jury):
    if choice == '1':
        print("Affichage des résultats des votes...")
        # Placeholder for actual result display logic
    elif choice == '2':
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
        if books:
            for book in books:
                print(f"Title: {book['title']}, Summary: {book['summary']}, Author: {book['author']}, Editor: {book['editor']}, Date: {book['publication_date']}, Pages: {book['pages']}, ISBN: {book['isbn']}, Price: {book['price']}")
        else:
            print("No books found for this selection.")
    elif choice == '2':
        title = input("Title of the book: ")
        author_name = input("Author's name: ")
        editor = input("Editor: ")
        summary = input("Summary: ")
        isbn = input("ISBN: ")
        publication_date = input("Publication Date (YYYY-MM-DD): ")
        pages = int(input("Number of pages: "))
        price = float(input("Price: "))
        # Here you should have logic to add the book to the selection
        print(f"Book added to selection.")
    elif choice == '3':
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
            name = input("Enter your name: ").strip()
            password = input("Enter your password: ").strip()
            member_data = members_dao.get_member_by_name(name)
            if member_data and member_data['password'] == password:
                if member_data['role'].lower() == "president":
                    member = President(name, password)
                    while True:
                        display_president_menu()
                        pres_choice = input("Choose an option: ").strip()
                        handle_president_choice(pres_choice, book_dao, member)
                elif member_data['role'].lower() == "jury":
                    member = Jury(name, password)
                    while True:
                        display_jury_menu()
                        jury_choice = input("Choose an option: ").strip()
                        handle_jury_choice(jury_choice, book_dao, member)
                elif member_data['role'].lower() == "member":
                    member = Member(name, password)
                    while True:
                        display_member_menu()
                        member_choice = input("Choose an option: ").strip()
                        handle_member_choice(member_choice)
                else:
                    print("Unknown role!")
            else:
                print("Invalid login credentials.")
        elif choice == '2':
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
