"""
The 'dobble' package provides functionalities for creating custom Dobble playing cards and decks.

It includes modules for defining project-level constants, handling circle packing data,
computing incidence matrices for finite projective planes, and creating Dobble playing cards and decks.

Modules:
    - constants: Defines project-level constants.
    - dobble: Contains functions to create individual Dobble playing cards and full decks of Dobble playing cards.
    - packing: Provides functions for handling circle packing data.
    - utils: Provides utility functions for finite projective planes.
"""

from . import constants
from ..organize_emojis import is_emojis_organized, organize_emojis

if not is_emojis_organized():
    organize_emojis('color')
    organize_emojis('black')

    with open(constants.EMOJIS_ORGANIZED_FLAG, "w") as flag_file:
        flag_file.write("Emojis have been organized.")
