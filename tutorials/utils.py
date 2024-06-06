"""Utility functions for use in the "tutorials/" Jupyter notebooks.

Functions:
    * display_card_inline: Display the playing card inline.
    * display_inline: Display the image inline.
    * draw_outline: Draw the outline of the playing card.
    * save_card_img: Save a playing card image to disk.
"""


import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


IMG_DIR = Path("../imgs")

__all__ = [
    "display_card_inline",
    "display_inline",
    "draw_outline",
    "save_card_img"
]


def display_card_inline(
        card_img: Image.Image,
        outline_width: int = 5
) -> None:
    """Display the playing card inline.

    Args:
        card_img: The playing card image to display.
        outline_width: The width of the playing card outline.
    """

    card_img = draw_outline(card_img, width=outline_width)
    display_inline(card_img)


def display_inline(img: Image.Image) -> None:
    """ Display the image inline.

    Args:
        img: The image to display.
    """

    img_np = np.array(img)
    _ = plt.imshow(img_np)
    _ = plt.axis('off')


def draw_outline(
        card_img: Image.Image,
        width: int = 5
) -> Image.Image:
    """Draw the outline of the playing card.

    Args:
        card_img: The playing card whose outline is to be drawn.
        width: The width of the playing card outline.

    Returns:
        The card image with the drawn outline.
    """

    draw = ImageDraw.Draw(card_img)
    img_size = card_img.size[0]
    draw.ellipse((0, 0, img_size - 1, img_size - 1), outline='black', width=width)
    return card_img


def save_card_img(
    card_img: Image.Image,
    filename: str,
    outline_width: int = 5,
    overwrite: bool = False
) -> None:
    """Save a playing card image to disk.

    Args:
        card_img: The playing card image to save.
        filename: The filename (without extension) under which to save
          the image.
        outline_width: The width of the playing card outline.
        overwrite: Whether to overwrite an already existing image.
    """

    filepath = IMG_DIR / f"{filename}.png"
    filepath.parent.mkdir(exist_ok=True, parents=True)
    card_img = draw_outline(card_img, width=outline_width)
    if not filepath.exists() or overwrite:
        card_img.save(filepath)
    else:
        warnings.warn(
            f"A file with the name '{filename}.png' already exists in '{filepath.parent}' and "
            "'overwrite' was set to False. The image was not saved."
        )


def create_card_img_from_group(
        group: str,
        num_emojis: int = 8,
        packing: str = "cci",
        seed: int = None
) -> Image.Image:
    """Create a playing card using emojis from the specified (sub)group.

    Args:
        group: The OpenMoji group or subgroup from which to choose the
          emojis.
        num_emojis: The number of emojis to place on the card.
        packing: The packing determining the layout of the card.
        seed: A seed to use in all non-deterministic operations in
          creating the card.

    Returns:
        The created playing Card as a PIL image.
    """

    # Retrieve names of all emojis in the (sub)group
    valid_group_passed = False
    try:
        all_emojis = utils.get_emoji_names_by_group(group)
        valid_group_passed = True
    except ValueError:
        pass

    if not valid_group_passed:
        try:
            all_emojis = utils.get_emoji_names_by_subgroup(group)
        except ValueError:
            raise ValueError(
                f"'{group}' is not the name of a group or subgroup in the OpenMoji dataset."
            )

    # Randomly pick ``num_emojis`` emojis and create card
    rng = np.random.default_rng(seed=seed)
    selected_emojis = rng.choice(all_emojis, num_emojis, replace=False).tolist()
    card = Card(selected_emojis, packing=packing)

    return card.get_img()
