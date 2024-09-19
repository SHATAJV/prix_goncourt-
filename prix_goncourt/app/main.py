from models.member import Member
from models.jury import Jury
from models.president import President
from dao.book_dao import BookDAO
from dao.members_dao import MembersDAO

def display_menu():
    print("=== Menu Principal ===")
    print("1. Login")
    print("2. Quitter")

def handle_login(member, book_dao):
    if isinstance(member, President):
        display_president_menu(book_dao, member)
    elif isinstance(member, Jury):
        display_jury_menu(book_dao, member)
    elif isinstance(member, Member):
        display_member_menu(book_dao)

def display_member_menu(book_dao):
    print("=== Menu Member ===")
    print("1. Afficher les livres d'une sélection")
    print("2. Quitter")
    choice = input("Choisissez une option: ")
    handle_member_choice(choice, book_dao)

def display_president_menu(book_dao, president):
    while True:
        print(f"=== Menu Président ({president.name}) ===")
        print("1. Ajouter des livres à la sélection")
        print("2. Afficher les résultats des votes")
        print("3. Quitter")
        choice = input("Choisissez une option: ")

        if choice == '1':
            selection_number = int(input("Numéro de la sélection (2 ou 3): "))
            book_ids = input("Entrez les ID des livres à ajouter (séparés par des virgules): ").split(',')
            book_ids = [int(book_id.strip()) for book_id in book_ids]
            book_dao.add_books_to_selection(selection_number, book_ids)
            print("Livres ajoutés à la sélection.")
        elif choice == '2':
            selection_number = int(input("Numéro de la sélection (2 ou 3): "))
            results = book_dao.get_vote_results_for_president(selection_number)
            for result in results:
                print(f"{result['title']} - {result['author']} - Votes: {result['votes_count']}")
        elif choice == '3':
            break
        else:
            print("Choix invalide.")

def display_jury_menu(book_dao, jury):
    while True:
        print(f"=== Menu Jury ({jury.name}) ===")
        print("1. Afficher les livres d'une sélection")
        print("2. Voter pour un livre")
        print("3. Quitter")
        choice = input("Choisissez une option: ")

        if choice == '1':
            selection_number = int(input("Entrez le numéro de la sélection (1, 2, 3): "))
            books = book_dao.get_books_by_selection(selection_number)
            if books:
                for book in books:
                    print(f"{book['title']} by {book['author']} - {book['summary'][:100]}...")
            else:
                print("Aucun livre disponible dans cette sélection.")
        elif choice == '2':
            book_id = int(input("Entrez l'ID du livre pour voter: "))
            book_dao.add_vote(book_id, jury.id_member)
            print("Vote ajouté avec succès!")
        elif choice == '3':
            break
        else:
            print("Choix invalide.")

def handle_member_choice(choice, book_dao):
    if choice == '1':
        selection_number = int(input("Entrez le numéro de la sélection (1, 2, 3): "))
        books = book_dao.read_books_by_selection(selection_number)
        if books:
            for book in books:
                print(f"ID: {book['id_book']}, Titre: {book['title']}, Auteur: {book['author']}")
        else:
            print("Aucun livre disponible dans cette sélection.")
    elif choice == '2':
        print("Goodbye!")
        exit()
    else:
        print("Choix invalide.")

def main():
    members_dao = MembersDAO()
    book_dao = BookDAO()  # Assurez-vous que BookDAO est correctement instancié

    while True:
        display_menu()
        option = input("Choisissez une option: ")

        if option == '1':
            name = input("Entrez votre nom: ")
            password = input("Entrez votre mot de passe: ")

            member_data = members_dao.get_member_by_name(name)
            if member_data:
                if member_data['password'] == password:
                    if member_data['role'] == 'president':
                        member = President(member_data['name'], member_data['password'], member_data['id_member'])
                        handle_login(member, book_dao)
                    elif member_data['role'] == 'jury':
                        member = Jury(member_data['name'], member_data['password'], member_data['id_member'])
                        handle_login(member, book_dao)
                    else:
                        print("Rôle inconnu.")
                else:
                    print("Mot de passe incorrect.")
            else:
                print("Identifiants incorrects.")
        elif option == '2':
            break
        else:
            print("Option non valide.")
if __name__ == "__main__":
    main()
