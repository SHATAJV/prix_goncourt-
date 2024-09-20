from models.member import Member

class Jury(Member):
    """
    Represents a jury member who can vote on books.

    Inherits from the Member class and includes voting capabilities.

    Attributes:
        name (str): The name of the jury member.
        password (str): The password of the jury member.
        id_member (int): The unique identifier for the jury member.
        role (str): The role of the member, defaults to 'jury'.
        vote_count (int): The total number of votes cast by the jury member.
    """

    def __init__(self, name, password, id_member, role='jury'):
        """
        Initializes a Jury instance.

        Args:
            name (str): The name of the jury member.
            password (str): The password of the jury member.
            id_member (int): The unique identifier for the jury member.
            role (str, optional): The role of the member. Defaults to 'jury'.
        """
        super().__init__(name, password, id_member, role)
        self.vote_count = 0  # Initialize vote count

    def vote(self, book, votes):
        """
        Records a vote for a given book.

        Args:
            book (Book): The book being voted for.
            votes (dict): A dictionary tracking the number of votes for each book.
        """
        if book in votes:
            votes[book] += 1
        else:
            votes[book] = 1
        self.vote_count += 1
        print(f"{self.name} voted for {book.title}")

    def __str__(self):
        """
        Returns a string representation of the jury member.

        Returns:
            str: A description of the jury member including their name.
        """
        return f"Jury: {self.name}"
