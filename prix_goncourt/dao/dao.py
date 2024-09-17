# -*- coding: utf-8 -*-

"""
Classe abstraite générique Dao[T], dont hérite les classes de DAO de chaque entité
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar, Optional
import pymysql.cursors


# ----- Database Connection -----
def get_db_connection():
    connection = pymysql.connector.connect(
        host="localhost",
        user="prix_goncourt",
        password="prix*goncourt224",
        database="prix_goncourt"
    )
    return connection
