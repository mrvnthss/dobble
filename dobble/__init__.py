"""
The "dobble" package allows users to create custom Dobble playing
cards and decks.

It provides the three classes "Emoji", "Card", and "Deck", representing
emojis, individual playing cards, and entire Dobble decks, respectively.
Supporting modules define project-level constants as well as utility
functions, and provide functionality to load circle packing data and to
compute incidence matrices of finite projective planes.

Modules:
    * card: Class to represent individual Dobble playing cards.
    * constants: Project-level constants.
    * deck: Class to represent Dobble decks.
    * emoji: Class to represent single emojis.
    * packings: Functionality to load circle packing data.
    * planes: Computes incidence matrices of finite projective planes.
    * utils: Utility functions.
    * visual: Base class for the Card and Emoji classes.
"""


from .card import Card
from .emoji import Emoji
