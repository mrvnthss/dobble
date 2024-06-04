"""A class representing a single emoji.

Typical usage example:

  >>> emoji = Emoji("unicorn")
  >>> emoji.rotate(-30)
  330
  >>> emoji.show(outline_only=True)
"""


from importlib.resources import files

import numpy as np
from PIL import Image
from PIL.Image import Resampling

from . import constants
from . import utils
from .visual import Visual


class Emoji(Visual):
    """A class representing a single emoji.

    Attributes:
        name: The name of the emoji.
        rotation: The counterclockwise rotation of the emoji in degrees.

    Methods:
        get_array(outline_only=False, padding=0, img_size=618): Get the
          emoji image as a NumPy array.
        get_img(outline_only=False, padding=0, img_size=618): Get the
          emoji image as a PIL Image.
        reset_rotation(): Reset the rotation of the emoji to 0 degrees.
        rotate(degrees, seed): Rotate the emoji by the specified number
          of degrees.
        show(outline_only=False, padding=0, img_size=618): Display the
          emoji image.
    """

    def __init__(
            self,
            name: str,
            rotation: float = 0
    ) -> None:
        """Initialize the emoji based on the OpenMoji name.

        Args:
            name: The name of the emoji.  Needs to be the name of one of
              the emojis included in the OpenMoji dataset.
            rotation: The counterclockwise rotation of the emoji in
              degrees.
        """

        if not utils.is_valid_emoji_name(name):
            raise ValueError(f"'{name}' is not a valid emoji name.")

        self.name = name
        super().__init__(rotation=rotation)

        self._group: str = utils.get_emoji_group(name)
        self._hexcode: str = utils.get_emoji_hexcode(name)

    def get_array(
            self,
            outline_only: bool = False,
            padding: float = 0,
            img_size: int = 618
    ) -> np.ndarray:
        return super().get_array(outline_only, padding, img_size)

    def get_img(
            self,
            outline_only: bool = False,
            padding: float = 0,
            img_size: int = 618
    ) -> Image.Image:
        """Get the emoji image as a PIL Image.

        Args:
            outline_only: Whether to return the outline-only version of
              the emoji.
            padding: The padding around the emoji image as a fraction of
              the image size.  Must be in the range [0, 1).
            img_size: The size of the square image in pixels.

        Returns:
            The emoji image as a PIL Image in RGBA mode.
        """

        # Load and rescale the emoji image
        img = self._load(outline_only=outline_only)
        img = utils.rescale_img(img, padding=padding)

        # Resize the image and rotate it, if necessary
        if img_size != constants.DEFAULT_IMG_SIZE:
            img = img.resize((img_size, img_size), resample=Resampling.LANCZOS)
        if self.rotation != 0:
            img = img.rotate(self.rotation, resample=Resampling.BICUBIC)

        return img

    def show(
            self,
            outline_only: bool = False,
            padding: float = 0,
            img_size: int = 618
    ) -> None:
        super().show(outline_only, padding, img_size)

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
        return Image.open(fpath).convert("RGBA")
