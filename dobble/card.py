"""A class representing an individual Dobble playing card.

Typical usage example:

  >>> dobble_card = Card(["unicorn", "dolphin", "cheese wedge", "bomb"])
"""


import warnings

from . import utils
from .emoji import Emoji


class Card:
    """A class representing an individual Dobble playing card.

    Attributes:
        emojis: A dictionary of the card's emojis.
        emoji_names: A list of names of the card's emojis.
        packing: The packing to place emojis on the card.
        rotation: The counterclockwise rotation of the playing card in
          degrees.

    Methods:
        reset_emoji_rotation(emoji_name): Reset the rotation of the
          specified emoji to 0 degrees.
        rotate_emoji(emoji_name, degrees): Rotate the specified emoji by
          the specified number of degrees.
    """

    def __init__(
            self,
            emoji_names: list[str],
            packing: str = "cci",
            rotation: float = 0
    ) -> None:
        """Initializes the instance based on the OpenMoji emoji names.

        Args:
            emoji_names: A list of emoji names.  Each name needs to be
              the name of one of the emojis included in the OpenMoji
              dataset.
            packing: The packing to place emojis on the playing card.
            rotation: The counterclockwise rotation of the playing card
              in degrees.
        """

        if not utils.is_valid_emoji_name(emoji_names):
            raise ValueError(
                "At least one of the emoji names is not valid or an empty list was passed."
            )

        unique_emoji_names = list(dict.fromkeys(emoji_names))
        if len(emoji_names) > len(unique_emoji_names):
            warnings.warn("Duplicate emoji names detected and removed.")
            emoji_names = unique_emoji_names

        if not utils.is_layout_available(packing, len(emoji_names)):
            if not utils.is_valid_packing(packing):
                raise ValueError(f"Packing '{packing}' is not available.")
            if len(emoji_names) > 50:
                raise ValueError("Cards with more than 50 emojis are not supported.")

            # If none of the errors above are raised, emoji_names has to be a list with 1 to 4
            # entries, all of which are valid emoji names.  In this case, we issue a warning and
            # revert to the 'cci' packing instead (only packing available for 1 to 4 emojis).
            warnings.warn(
                f"Packing '{packing}' is not available for cards with {len(emoji_names)} "
                f"emojis. Using 'cci' instead."
            )

        self.emoji_names = emoji_names
        self.packing = packing
        self.rotation = rotation

        self.emojis = {name: Emoji(name) for name in emoji_names}

    def rotate_emoji(
            self,
            emoji_name: str,
            degrees: float
    ) -> None:
        """Rotate the specified emoji.

        Args:
            emoji_name: The name of the emoji to rotate.
            degrees: The number of degrees to rotate the emoji.
        """

        self.emojis[emoji_name].rotate(degrees)

    def reset_emoji_rotation(
            self,
            emoji_name: str
    ) -> None:
        """Reset the rotation of the specified emoji to 0 degrees.

        Args:
            emoji_name: The name of the emoji to reset.
        """

        self.emojis[emoji_name].reset_rotation()
