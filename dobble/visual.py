"""A base class for visual elements."""


from abc import ABC, abstractmethod

import numpy as np
from PIL import Image


class Visual(ABC):
    """A base class for visual elements.

    This class serves as a base class for the Card and Emoji classes.

    Note:
        This class is not intended to be used directly by the user.

    Attributes:
        rotation: The counterclockwise rotation of the visual element in
          degrees.

    Methods:
        get_array(outline_only, padding, img_size): Get the image as a
          NumPy array.
        get_img(outline_only, padding, img_size): Get the image as a PIL
          Image.
        reset_rotation(): Reset the rotation of the visual element to 0
          degrees.
        rotate(degrees, seed): Rotate the visual element by the
          specified number of degrees.
        show(outline_only, padding, img_size): Display the image.
    """

    def __init__(
            self,
            rotation: float = 0
    ) -> None:
        """Initialize the visual element.

        Args:
            rotation: The counterclockwise rotation of the visual
              element in degrees.
        """

        self.rotation = rotation % 360

    @abstractmethod
    def get_img(
            self,
            outline_only: bool,
            padding: float,
            img_size: int
    ) -> Image.Image:
        """Get the image as a PIL Image.

        Note:
            This method needs to be implemented in each subclass.

        Args:
            outline_only: Whether to return/use the outline-only version
              of the emoji image(s).
            padding: The padding around the emoji image as a fraction
              of the image size.  Must be in the range [0, 1).
            img_size: The size of the square image in pixels.

        Returns:
            The image as a PIL Image in RGBA mode.
        """

    def get_array(
            self,
            outline_only: bool,
            padding: float,
            img_size: int
    ) -> np.ndarray:
        """Get the image as a NumPy array.

        This method calls the ``get_img`` method and converts the
        resulting PIL Image to a NumPy array.

        Args:
            outline_only: Whether to return/use the outline-only version
              of the emoji image(s).
            padding: The padding around the emoji image as a fraction
              of the image size.  Must be in the range [0, 1).
            img_size: The size of the square image in pixels.

        Returns:
            The image as a NumPy array.
        """

        img = self.get_img(
            outline_only=outline_only,
            padding=padding,
            img_size=img_size
        )
        return np.array(img)

    def reset_rotation(self) -> None:
        """Reset the rotation of the visual element to 0 degrees."""

        self.rotation = 0

    def rotate(
            self,
            degrees: float = None,
            seed: int = None
    ) -> float:
        """Rotate the visual element by the specified number of degrees.

        If the ``degrees`` argument is not provided, the visual element
        is rotated by a random number of degrees in the range [0, 360)
        using the provided seed.

        Args:
            degrees: The number of degrees to rotate the visual element
              by.  Positive values lead to a counterclockwise rotation,
              while negative values lead to a clockwise rotation.
            seed: The seed to use for the random number generator that's
              used to determine the rotation angle, in case the latter
              is not provided.

        Returns:
            The new rotation of the visual element.
        """

        if degrees is not None:
            self.rotation = (self.rotation + degrees) % 360
        else:
            rng = np.random.default_rng(seed)
            self.rotation = rng.uniform(0, 360)
        return self.rotation

    def show(
            self,
            outline_only: bool,
            padding: float,
            img_size: int
    ) -> None:
        """Display the image.

        This method calls the ``get_img`` method and displays the
        resulting PIL Image.

        Args:
            outline_only: Whether to return/use the outline-only version
              of the emoji image(s).
            padding: The padding around the emoji image as a fraction
              of the image size.  Must be in the range [0, 1).
            img_size: The size of the square image in pixels.
        """

        self.get_img(
            outline_only=outline_only,
            padding=padding,
            img_size=img_size
        ).show()
