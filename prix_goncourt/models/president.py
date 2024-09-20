from models.member import Member

class President(Member):
    """
    Represents the president of the selection committee.

    Inherits from the Member class and includes functionalities to manage selections and announce results.

    Attributes:
        name (str): The name of the president.
        password (str): The password of the president.
        id_member (int): The unique identifier for the president.
        role (str): The role of the member, defaults to 'president'.
    """

    def __init__(self, name, password, id_member, role='president'):
        """
        Initializes a President instance.

        Args:
            name (str): The name of the president.
            password (str): The password of the president.
            id_member (int): The unique identifier for the president.
            role (str, optional): The role of the member. Defaults to 'president'.
        """
        super().__init__(name, password, id_member, role)
        self.id_member = id_member

    def manage_selections(self, selection):
        """
        Manages book selections for a given selection round.

        Args:
            selection (Selection): The selection object containing selection details.
        """
        print(f"Managing selections for tour {selection.selection_number}:")
        for book in selection.books:
            print(f" - {book.title}")

    def result(self, book_votes):
        """
        Announce the voting results and determine the winner.

        Args:
            book_votes (dict): A dictionary mapping books to their vote counts.
        """
        print("Result:")
        winner = max(book_votes, key=book_votes.get)
        for book, vote_count in book_votes.items():
            print(f"{book.title}: {vote_count} votes")
        print(f"The winner is {winner.title}!")

    def __str__(self):
        """
        Returns a string representation of the president.

        Returns:
            str: A description of the president including their name.
        """
        return f"President: {self.name}"
