"""A class representing an individual Dobble playing card.

Typical usage example:

  >>> emoji_names = ["light bulb", "sun", "maple leaf", "unicorn", "bomb"]
  >>> dobble_card = Card(emoji_names, packing="ccir")
  >>> dobble_card.rotate_emojis(seed=42)
  >>> dobble_card.show()
  >>> dobble_card_np = dobble_card.get_array()
"""


import warnings

import numpy as np
from PIL import Image, ImageDraw
from PIL.Image import Resampling

from . import packings
from . import utils
from .emoji import Emoji
from .visual import Visual


class Card(Visual):
    """A class representing an individual Dobble playing card.

    Attributes:
        emojis: A dictionary of the card's emojis.
        emoji_names: A list of names of the card's emojis.
        num_emojis: The number of emojis on the card.
        packing: The packing determining the layout of the card.
        rotation: The counterclockwise rotation of the playing card in
          degrees.

    Methods:
        get_array(outline_only=False, padding=0.05, img_size=1024): Get
          the card image as a NumPy array.
        get_img(outline_only=False, padding=0.05, img_size=1024): Get
          the card image as a PIL Image.
        reset_emoji_rotations(emoji_names=None): Reset the rotation of
          the specified emoji(s) to 0 degrees.
        reset_rotation(): Reset the rotation of the playing card to 0
          degrees.
        rotate(degrees, seed): Rotate the playing card by the specified
          number of degrees.
        rotate_emojis(emoji_data=None, seed=None): Rotate the specified
          emoji(s).
        show(outline_only=False, padding=0.05, img_size=1024): Display
          the card image.
        shuffle_emojis(permutation=None, seed=None): Shuffle the emojis
          on the card.
    """

    def __init__(
            self,
            emoji_names: list[str],
            packing: str = "cci",
            rotation: float = 0
    ) -> None:
        """Initialize the playing card.

        Args:
            emoji_names: A list of emoji names.  Each name needs to be
              the name of one of the emojis included in the OpenMoji
              dataset.
            packing: The packing determining the layout of the card.
            rotation: The counterclockwise rotation of the playing card
              in degrees.
        """

        # Validate emoji names
        if not utils.is_valid_emoji_name(emoji_names):
            raise ValueError(
                "At least one of the emoji names is not valid or an empty list was passed."
            )

        # Remove duplicate emoji names, if any
        unique_emoji_names = list(dict.fromkeys(emoji_names))
        if len(emoji_names) > len(unique_emoji_names):
            warnings.warn("Duplicate emoji names detected and removed.")
            emoji_names = unique_emoji_names

        # Check if the packing is available
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
        super().__init__(rotation=rotation)

        self.emojis = {name: Emoji(name) for name in emoji_names}
        self.num_emojis = len(emoji_names)

    def get_array(
            self,
            outline_only: bool = False,
            padding: float = 0.05,
            img_size: int = 1024
    ) -> np.ndarray:
        return super().get_array(outline_only, padding, img_size)

    def get_img(
            self,
            outline_only: bool = False,
            padding: float = 0.05,
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

        Raises:
            ValueError: If the padding is not in the range [0, 1) or if
              the image size is not a positive integer.
        """

        # Check if padding is within valid range
        if not 0 <= padding < 1:
            raise ValueError("Padding must be in the range [0, 1).")

        # Check if the image size is a positive integer
        if not utils.is_integer(img_size) or img_size < 1:
            raise ValueError(f"Image size must be a positive integer, got {img_size}.")

        # Create empty playing card
        img = Image.new("RGBA", (img_size, img_size))
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, img_size - 1, img_size - 1), fill="white")

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

        # Apply rotation, if necessary
        if self.rotation != 0:
            img = img.rotate(self.rotation, resample=Resampling.BICUBIC)

        return img

    def reset_emoji_rotations(
            self,
            emoji_names: str | list[str] = None
    ) -> None:
        """Reset the rotation of the specified emoji(s) to 0 degrees.

        Args:
            emoji_names: The name of the emoji or a list of names of
              emojis to reset the rotation of.  If None, the rotation of
              all emojis is reset to 0 degrees.

        Raises:
            ValueError: If ``emoji_names`` is neither a string, a list
              of strings, nor None.  Also raised if at least one of the
              emoji names is not the name of an emoji on the card.
        """

        def reset_rotation_of_single_emoji(emoji_name: str) -> None:
            """Helper function to reset the rotation of a single emoji."""

            if emoji_name in self.emojis:
                self.emojis[emoji_name].reset_rotation()
            else:
                raise ValueError(f"Emoji '{emoji_name}' not found on card.")

        if emoji_names is None:
            for emoji in self.emojis:
                reset_rotation_of_single_emoji(emoji)
        elif isinstance(emoji_names, str):
            reset_rotation_of_single_emoji(emoji_names)
        elif isinstance(emoji_names, list):
            for name in emoji_names:
                reset_rotation_of_single_emoji(name)
        else:
            raise ValueError("Invalid input.")

    def rotate_emojis(
            self,
            emoji_data: tuple[str, float] | list[tuple[str, float]] = None,
            seed: int = None
    ) -> None:
        """Rotate the specified emoji(s).

        Rotate selected emojis on the card by a specified number of
        degrees.

        Args:
            emoji_data: A tuple or list of tuples, each containing the
                name of an emoji of the card and the number of degrees
                to rotate it by.  If None, all emojis are rotated
                randomly.
            seed: If no emoji data is passed, a seed can be passed to
                initialize the random number generator, which is used to
                rotate the emojis, allowing for reproducible rotations.

        Raises:
            ValueError: If ``emoji_data`` is neither a tuple of length
              2, a list of tuples of length 2, nor None.  Also raised if
              at least one of the emoji names is not the name of an
              emoji on the card.
        """

        def rotate_single_emoji(
                emoji_name: str,
                degrees: float
        ) -> None:
            """Helper function to rotate a single emoji."""

            if emoji_name in self.emojis:
                _ = self.emojis[emoji_name].rotate(degrees)
            else:
                raise ValueError(f"Emoji '{emoji_name}' not found on card.")

        def rotate_all() -> None:
            """Helper function to rotate all emojis randomly."""

            rng = np.random.default_rng(seed=seed)
            for emoji in self.emojis.values():
                _ = emoji.rotate(rng.uniform(0, 360))

        if emoji_data is None:
            rotate_all()
        elif isinstance(emoji_data, tuple) and len(emoji_data) == 2:
            rotate_single_emoji(*emoji_data)
        elif isinstance(emoji_data, list):
            for emoji_tuple in emoji_data:
                if isinstance(emoji_tuple, tuple) and len(emoji_tuple) == 2:
                    rotate_single_emoji(*emoji_tuple)
                else:
                    raise ValueError(
                        "At least one of the entries in the list is not a tuple of length 2."
                    )
        else:
            raise ValueError("Invalid input.")

    def show(
            self,
            outline_only: bool = False,
            padding: float = 0.05,
            img_size: int = 1024
    ):
        super().show(outline_only, padding, img_size)

    def shuffle_emojis(
            self,
            permutation: list[int] = None,
            seed: int = None
    ) -> list[str]:
        """Shuffle the emojis on the card.

        Args:
            permutation: A permutation of the integers from 1 to the
              number of emojis on the card.  If None, the emojis are
              shuffled randomly.
            seed: If no permutation is passed, a seed can be passed to
              initialize the random number generator, which is used to
              shuffle the emojis, allowing for reproducible shuffling.

        Returns:
            The shuffled list of emoji names.

        Raises:
            ValueError: If the permutation is not valid.

        Examples:
            >>> dobble_card = Card(["unicorn", "dolphin", "cheese wedge", "bomb"])
            >>> dobble_card.shuffle_emojis(permutation=[2, 3, 4, 1])
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

        return self.emoji_names
