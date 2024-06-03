"""A class representing an individual Dobble playing card.

Typical usage example:

  >>> emoji_names = ["light bulb", "sun", "maple leaf", "unicorn", "bomb"]
  >>> dobble_card = Card(emoji_names, packing="ccir")
"""


import warnings

import numpy as np
from PIL import Image, ImageDraw
from PIL.Image import Resampling

from . import packings
from . import utils
from .emoji import Emoji


class Card:
    """A class representing an individual Dobble playing card.

    Attributes:
        emojis: A dictionary of the card's emojis.
        emoji_names: A list of names of the card's emojis.
        num_emojis: The number of emojis on the card.
        packing: The packing determining the layout of the card.
        rotation: The counterclockwise rotation of the playing card in
          degrees.

    Methods:
        get_img(outline_only=False, padding=0.01, img_size=1024): Get
          the card image as a PIL Image.
        reset_emoji_rotation(emoji_name): Reset the rotation of the
          specified emoji to 0 degrees.
        reset_rotation(): Reset the rotation of the playing card to 0
          degrees.
        rotate(degrees): Rotate the playing card by the specified number
          of degrees.
        rotate_emoji(emoji_name, degrees): Rotate the specified emoji by
          the specified number of degrees.
        shuffle_emojis(permutation=None, seed=None): Shuffle the emojis
          on the card.
    """

    def __init__(
            self,
            emoji_names: list[str],
            packing: str = "cci",
            rotation: float = 0
    ) -> None:
        """Initialize the instance based on the OpenMoji emoji names.

        Args:
            emoji_names: A list of emoji names.  Each name needs to be
              the name of one of the emojis included in the OpenMoji
              dataset.
            packing: The packing determining the layout of the card.
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

            # If none of the errors above are raised, ``emoji_names`` has to be a list with 1 to 4
            # entries, all of which are valid emoji names.  In this case, we issue a warning and
            # revert to the "cci" packing instead (only packing available for 1 to 4 emojis).
            warnings.warn(
                f"Packing '{packing}' is not available for cards with {len(emoji_names)} "
                f"emojis. Using 'cci' instead."
            )

        self.emoji_names = emoji_names
        self.packing = packing
        self.rotation = rotation

        self.emojis = {name: Emoji(name) for name in emoji_names}
        self.num_emojis = len(emoji_names)

    def get_img(
            self,
            outline_only: bool = False,
            padding: float = 0.01,
            img_size: int = 1024
    ) -> Image.Image:
        """Get the card image as a PIL Image.

        Args:
            outline_only: Whether to use the outline-only version of the
              emojis.
            padding: The padding around each emoji image as a fraction
              of the image size.  Must be in the range [0, 1).
            img_size: The size of the square image in pixels.

        Returns:
            The card image as a PIL Image in RGBA mode.
        """

        # Create empty playing card
        img = Image.new("RGBA", (img_size, img_size))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, img_size, img_size), fill="white")

        # Retrieve packing data
        packing_data = packings.get_packing_data(
            num_circles=self.num_emojis,
            packing=self.packing,
            img_size=img_size
        )
        coordinates = packing_data["coordinates"]
        radii = packing_data["radii"]

        # Place emojis on card
        for idx, emoji_name in enumerate(self.emoji_names):
            # Retrieve, resize, and paste emoji image
            emoji = self.emojis[emoji_name]
            emoji_img_size = int(2 * radii[idx])
            emoji_img = emoji.get_img(
                outline_only=outline_only,
                padding=padding,
                img_size=emoji_img_size
            )
            img.paste(
                emoji_img,
                tuple(coordinates[idx] - radii[idx]),  # upper left corner
                mask=emoji_img
            )

        # Apply rotation
        img = img.rotate(self.rotation, resample=Resampling.BICUBIC)

        return img

    def reset_emoji_rotation(
            self,
            emoji_name: str
    ) -> None:
        """Reset the rotation of the specified emoji to 0 degrees.

        Args:
            emoji_name: The name of the emoji to reset.
        """

        self.emojis[emoji_name].reset_rotation()

    def reset_rotation(self) -> None:
        """Reset the rotation of the playing card to 0 degrees."""

        self.rotation = 0

    def rotate(
            self,
            degrees: float
    ) -> None:
        """Rotate the playing card by the specified number of degrees.

        Args:
            degrees: The number of degrees to rotate the playing card
              by.  Positive values rotate the playing card
              counterclockwise, while negative values lead to a
              clockwise rotation.
        """

        self.rotation = (self.rotation + degrees) % 360

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

    def shuffle_emojis(
            self,
            permutation: list[int] = None,
            seed: int = None
    ) -> None:
        """Shuffle the emojis on the card.

        Args:
            permutation: A permutation of the integers from 1 to the
              number of emojis on the card.  If None, the emojis are
              shuffled randomly.
            seed: If no permutation is passed, a seed can be passed to
              initialize the random number generator, which is used to
              shuffle the emojis, allowing for reproducible shuffling.

        Raises:
            ValueError: If the permutation is not valid.

        Examples:
            >>> card = Card(["unicorn", "dolphin", "cheese wedge", "bomb"])
            >>> card.shuffle_emojis(permutation=[2, 3, 4, 1])
            >>> card.emoji_names
            ['dolphin', 'cheese wedge', 'bomb', 'unicorn']
        """

        if permutation:
            if not (len(permutation) == self.num_emojis
                    and utils.is_valid_permutation(permutation)):
                raise ValueError("Invalid permutation.")
            self.emoji_names = [self.emoji_names[i - 1] for i in permutation]
        else:
            rng = np.random.default_rng(seed=seed)
            rng.shuffle(self.emoji_names)
