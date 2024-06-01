"""A class representing a single emoji.

Typical usage example:

  >>> emoji = Emoji("unicorn")
  >>> emoji.rotate(-30)
  >>> emoji.show(outline_only=True)
"""


from importlib.resources import files

import numpy as np
from PIL import Image

from . import constants
from . import utils


class Emoji:
    """A class representing a single emoji.

    Attributes:
        name: The name of the emoji.
        rotation: The counterclockwise rotation of the emoji in degrees.

    Methods:
        get_array(outline_only=False, padding=0): Get the emoji image
          as a NumPy array.
        get_img(outline_only=False, padding=0): Get the emoji image as
          a PIL Image.
        reset_rotation(): Reset the rotation of the emoji to 0 degrees.
        rotate(degrees): Rotate the emoji by the specified number of
          degrees.
        show(outline_only=False, padding=0): Display the emoji image.
    """

    def __init__(
            self,
            name: str,
            rotation: float = 0
    ) -> None:
        """Initialize the instance based on the OpenMoji emoji name.

        Args:
            name: The name of the emoji.  Needs to be the name of one of
              the emojis included in the OpenMoji dataset.
            rotation: The counterclockwise rotation of the emoji in
              degrees.
        """

        if not utils.is_valid_emoji_name(name):
            raise ValueError(f"'{name}' is not a valid emoji name.")

        self.name = name
        self.rotation = rotation

        self._group: str = utils.get_emoji_group(name)
        self._hexcode: str = utils.get_emoji_hexcode(name)

    def rotate(
            self,
            degrees: float
    ) -> None:
        """Rotate the emoji by the specified number of degrees.

        Args:
            degrees: The number of degrees to rotate the emoji by.
              Positive values rotate the emoji counterclockwise, while
              negative values lead to a clockwise rotation.
        """

        self.rotation = (self.rotation + degrees) % 360

    def reset_rotation(self) -> None:
        """Reset the rotation of the emoji to 0 degrees."""

        self.rotation = 0

    def get_img(
            self,
            outline_only: bool = False,
            padding: float = 0
    ) -> Image.Image:
        """Get the emoji image as a PIL Image.

        Args:
            outline_only: Whether to return the outline-only version of
              the emoji.
            padding: The padding around the image content as a fraction
              of the image size.  Must be in the range [0, 1).

        Returns:
            The emoji image as a PIL Image in RGBA mode.
        """

        img = self._load(outline_only=outline_only)
        img = utils.rescale_img(img, padding=padding)
        img = img.rotate(self.rotation)

        return img

    def get_array(
            self,
            outline_only: bool = False,
            padding: float = 0
    ) -> np.ndarray:
        """Get the emoji image as a NumPy array.

        This method calls the ``get_img`` method and converts the
        resulting PIL Image to a NumPy array.

        Args:
            outline_only: Whether to return the outline-only version of
              the emoji.
            padding: The padding around the image content as a fraction
              of the image size.  Must be in the range [0, 1).

        Returns:
            The emoji image as a NumPy array.
        """

        img = self.get_img(
            outline_only=outline_only,
            padding=padding
        )
        return np.array(img)

    def show(
            self,
            outline_only: bool = False,
            padding: float = 0
    ) -> None:
        """Display the emoji image.

        This method calls the ``get_img`` method and displays the
        resulting PIL Image.

        Args:
            outline_only: Whether to display the outline-only version of
              the emoji.
            padding: The padding around the image content as a fraction
              of the image size.  Must be in the range [0, 1).
        """

        self.get_img(
            outline_only=outline_only,
            padding=padding
        ).show()

    def _load(
            self,
            outline_only: bool = False
    ) -> Image.Image:
        """Load the emoji image.

        Args:
            outline_only: Whether to load the outline-only version of
              the emoji.

        Returns:
            The emoji image as a PIL Image in RGBA mode.
        """

        color = "black" if outline_only else "color"
        fpath = files(constants.OPENMOJI_DIR) / color / self._group / f"{self._hexcode}.png"
        img = Image.open(fpath).convert("RGBA")

        return img
