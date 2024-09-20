# -*- coding: utf-8 -*-


class Author:
    """
    Represents an author with a name and an optional biography.

    Attributes:
        name (str): The name of the author.
        biography (str, optional): A brief biography of the author.
    """

    def __init__(self, name, biography=None):
        """
        Initializes an Author instance.

        Args:
            name (str): The name of the author.
            biography (str, optional): A brief biography of the author. Defaults to None.
        """
        self.name = name
        self.biography = biography

    def __str__(self):
        """
        Returns a string representation of the author.

        Returns:
            str: A string indicating the author's name.
        """
        return f"Author {self.name}"
