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
    print("=== Member Menu ===")
    print("1. Afficher les livres d'une sélection")
    print("2. Quitter")
    choice = input("Choisissez une option: ")
    handle_member_choice(choice, book_dao)

def display_jury_menu(book_dao, jury):
    print("=== Jury Menu ===")
    print("1. Afficher les livres d'une sélection")
    print("2. Voter pour des livres")
    print("3. Quitter")
    choice = input("Choisissez une option: ")
    handle_jury_choice(choice, book_dao, jury)

def display_president_menu(book_dao, president):
    print("=== President Menu ===")
    print("1. Afficher les résultats des votes pour une sélection")
    print("2. Ajouter des livres à une sélection")
    print("3. Quitter")
    choice = input("Choisissez une option: ")
    handle_president_choice(choice, book_dao, president)

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

def handle_jury_choice(choice, book_dao, jury):
    if choice == '1':
        selection_number = int(input("Entrez le numéro de la sélection (1, 2, 3): "))
        books = book_dao.read_books_by_selection(selection_number)
        if books:
            for book in books:
                print(f"ID: {book['id_book']}, Titre: {book['title']}, Auteur: {book['author']}")
        else:
            print("Aucun livre disponible dans cette sélection.")
    elif choice == '2':
        print("Vote pour des livres...")
        id_book = int(input("Entrez l'ID du livre pour lequel vous votez: "))
        book_dao.add_vote(id_book, jury.id_member)
        print("Vote ajouté avec succès!")
    elif choice == '3':
        print("Goodbye!")
        exit()
    else:
        print("Choix invalide.")

def handle_president_choice(choice, book_dao, president):
    if choice == '1':
        selection_number = int(input("Entrez le numéro de la sélection (1, 2, 3): "))
        vote_results = book_dao.get_vote_results_for_president(selection_number)
        if vote_results:
            for result in vote_results:
                print(f"Livre : {result['title']}, Auteur : {result['author']}, Nombre de votes : {result['votes_count']}")
        else:
            print("Aucun résultat de vote pour cette sélection.")
    elif choice == '2':
        # Logique pour ajouter des livres à une sélection
        pass
    elif choice == '3':
        print("Goodbye!")
        exit()
    else:
        print("Choix invalide.")


def main():
    book_dao = BookDAO()
    members_dao = MembersDAO()

    while True:
        display_menu()
        choice = input("Choisissez une option: ")
        if choice == '1':
            name = input("Entrez votre nom: ")
            password = input("Entrez votre mot de passe: ")

            # Récupérer les informations du membre depuis la base de données
            member_data = members_dao.get_member_by_name(name)

            # Vérifier si les identifiants sont corrects
            if member_data and member_data['password'] == password:

                # Vérification du rôle du membre
                if member_data['role'].lower() == "president":
                    member = President(member_data['name'], member_data['password'])
                elif member_data['role'].lower() == "jury":
                    member = Jury(member_data['name'], member_data['password'])
                else:
                    member = Member(member_data['name'], member_data['password'])

                # Afficher le menu correspondant au rôle
                handle_login(member, book_dao)
            else:
                print("Identifiants incorrects.")
        elif choice == '2':
            print("Goodbye!")
            exit()
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()
