"""Utility functions used in the "dobble" package.

Functions:
    * is_integer: Check if a number is an integer.
    * is_prime: Check if a number is prime.
    * is_prime_power: Check if a number is a prime power.
    * rescale_img: Rescale a square image to fit content within
        inscribed circle.
    * is_valid_emoji_name: Check if emojis exist in the OpenMoji
        dataset.
    * get_emoji_group: Get the "group" attribute of an emoji.
    * get_emoji_hexcode: Get the "hexcode" attribute of an emoji.
    * is_valid_packing: Check if a packing is valid (i.e., implemented).
    * is_layout_available: Check if a layout is available.
"""


from importlib.resources import files
import json
import math

import numpy as np
from PIL import Image

from . import constants


# Load OpenMoji metadata from restructured JSON file
json_fpath = files(constants.OPENMOJI_DIR) / "openmoji_restructured.json"
with json_fpath.open("r", encoding="utf-8") as json_file:
    _META_DATA = json.load(json_file)


def is_integer(num: int | float) -> bool:
    """Check if a number is an integer.

    Args:
        num: The number to be checked.

    Returns:
        True if ``num`` is an integer, False otherwise.
    """

    return isinstance(num, int) or (isinstance(num, float) and num.is_integer())


def is_prime(num: int | float) -> bool:
    """Check if a number is prime.

    Args:
        num: The number to be checked.

    Returns:
        True if ``num`` is a prime number, False otherwise.
    """

    state = True

    if not is_integer(num) or num <= 1:
        state = False
    else:
        # Check for non-trivial factors
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                state = False
                break
    return state


def is_prime_power(num: int | float) -> bool:
    """Check if a number is a prime power.

    Args:
        num: The number to be checked.

    Returns:
        True if ``num`` is a prime power, False otherwise.
    """

    state = False

    if is_integer(num) and num > 1:
        # Compute the i-th root of ``num`` and check if it's prime
        for i in range(1, int(math.log2(num)) + 1):
            root = num ** (1 / i)
            if is_integer(root) and is_prime(root):
                state = True
                break
    return state


def rescale_img(
        img: Image.Image,
        padding: float = 0.1
) -> Image.Image:
    """Rescale a square image to fit content within inscribed circle.

    This function expects as input a square image in RGBA mode, and
    rescales the image such that all non-transparent content fits
    within the inscribed circle.  The padding argument specifies the
    fraction of the image size to be added as padding around the image
    content.

    Args:
        img: The square image whose content is to be rescaled.
        padding: The padding around the image content as a fraction of
          the image size.  Must be in the range [0, 1).

    Returns:
        The image in RGBA mode with rescaled content, but identical
        dimensions.

    Raises:
        ValueError: If the image is not a square image in RGBA mode or
          if the padding is not in the range [0, 1).
    """

    # Check if image is in RGBA mode
    if img.mode != "RGBA":
        raise ValueError("Image must be in RGBA mode.")

    # Convert image to NumPy array, then check if it's a square image
    img_np = np.array(img)
    if img_np.shape[0] != img_np.shape[1]:
        raise ValueError("Image must be a square image.")

    # Check if padding is within valid range
    if not 0 <= padding < 1:
        raise ValueError("Padding must be in the range [0, 1).")

    # Determine non-transparent pixels, and return image if all pixels are transparent
    non_transparent = np.argwhere(img_np[:, :, -1] > 0)
    if non_transparent.shape[0] == 0:
        return img

    # Determine Euclidean distance (in pixels) of outermost non-transparent pixel
    img_size = img_np.shape[0]
    radius = img_size // 2
    non_transparent = non_transparent - radius + 0.5  # shift center to (0, 0)
    max_distance = np.max(np.linalg.norm(non_transparent, axis=1))

    # Compute target size in pixels
    rescaling_factor = (1 - padding) * radius / max_distance
    target_size = int(img_size * rescaling_factor)

    # Rescale image
    if img_size == target_size:
        return img
    img = img.resize((target_size, target_size))

    # Offset to center rescaled image on canvas / crop rescaled image to fit original canvas
    offset = abs(img_size - target_size) // 2

    if target_size < img_size:  # paste rescaled smaller image onto canvas of original size
        canvas = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
        canvas.paste(img, (offset, offset), mask=img)
        img = canvas
    elif target_size > img_size:  # crop rescaled larger image to fit original canvas
        img = img.crop((offset, offset, offset + img_size, offset + img_size))

    return img


def is_valid_emoji_name(emoji_name: str | list[str]) -> bool:
    """Check if emojis exist in the OpenMoji dataset.

    Args:
        emoji_name: The emoji name or a list of emoji names to be
          checked.

    Returns:
        True if the emoji or all emojis in the list exist in the
        OpenMoji dataset, False otherwise.  Returns False for empty
        lists.
    """

    if isinstance(emoji_name, list):
        if len(emoji_name) == 0:
            return False
        return all(name in _META_DATA for name in emoji_name)

    return emoji_name in _META_DATA


def get_emoji_group(emoji_name: str) -> str:
    """Get the "group" attribute of an emoji.

    Args:
        emoji_name: The emoji name.

    Returns:
        The "group" attribute of the emoji.

    Raises:
        ValueError: If the emoji name is not valid.
    """

    if not is_valid_emoji_name(emoji_name):
        raise ValueError(f"'{emoji_name}' is not a valid emoji name.")

    return _META_DATA[emoji_name]["group"]


def get_emoji_hexcode(emoji_name: str) -> str:
    """Get the "hexcode" attribute of an emoji.

    Args:
        emoji_name: The emoji name.

    Returns:
        The "hexcode" attribute of the emoji.

    Raises:
        ValueError: If the emoji name is not valid.
    """

    if not is_valid_emoji_name(emoji_name):
        raise ValueError(f"'{emoji_name}' is not a valid emoji name.")

    return _META_DATA[emoji_name]["hexcode"]


def is_valid_packing(packing: str) -> bool:
    """Check if the provided packing is valid (i.e., implemented).

    Args:
        packing: Type of circle packing.

    Returns:
        True if the packing is valid, False otherwise.
    """

    return packing.lower() in constants.PACKINGS_DICT


def is_layout_available(
        packing: str,
        num_circles: int
) -> bool:
    """Check if a layout is available.

    This function checks whether a particular combination of packing
    type and number of circles is available.

    Args:
        packing: Type of circle packing.
        num_circles: Total number of circles in the packing.

    Returns:
        True if the layout is available, False otherwise.
    """

    is_num_circles_valid = is_integer(num_circles) and num_circles > 0

    if not is_valid_packing(packing) or not is_num_circles_valid:
        return False

    return num_circles in constants.PACKINGS_DICT[packing.lower()][1]
