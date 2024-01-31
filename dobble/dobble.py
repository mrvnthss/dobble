"""Module for creating custom Dobble playing cards and decks.

This module contains functions to create individual Dobble playing cards
and full decks of Dobble playing cards.

Functions:
    - _create_empty_card: Create a square image of a white disk against
        a transparent background.
    - _get_hex_codes: Retrieve the hex codes of all emojis in a group.
    - _load_emoji: Load an emoji into memory.
    - _rescale_emoji: Rescale an emoji so that it fits inside the circle
        inscribed in a square image.
    - _place_emoji: Place an emoji on a card image at specified
        coordinates with the specified size.
    - create_dobble_card: Create a single Dobble playing card.
    - create_dobble_deck: Create a full deck of Dobble playing cards.

The module uses the "packing" and "utils" modules from the "dobble"
package to arrange the emojis on the cards and to compute the incidence
matrices for finite projective planes, respectively.  The latter is used
to determine which emojis are placed on which cards in order to create a
valid Dobble deck.
"""

# Standard Library Imports
import csv
import io
import os
import random
from importlib import resources

# Third-Party Library Imports
from PIL import Image, ImageDraw
import numpy as np
import pandas as pd

# Local Imports
from . import constants
from . import packing
from . import utils


def _create_empty_card(image_size: int, return_pil: bool = True) -> Image.Image | np.ndarray:
    """Create a square image of a white disk w/ transparent background.

    Args:
        image_size (int): The size of the square image in pixels.
        return_pil (bool): Whether to return a PIL Image (True) or a
            NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The generated image of a white disk
            against a transparent background.
    """
    # Create a new transparent image with RGBA mode
    image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))

    # Create a new draw object and draw a white disk onto the image
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, image_size, image_size), fill=(255, 255, 255, 255))

    return image if return_pil else np.array(image)


def _get_hex_codes(mode: str, group: str) -> list[str]:
    """Retrieve the hex codes of all emojis in a group.

    Args:
        mode (str): The mode of the emojis.  Either "color" or "black".
        group (str): The name of the group of emojis.

    Returns:
        list[str]: A list of hex codes of all emojis (of the specified
            mode) in the group.
    """
    # Ensure that the specified mode is valid
    if mode not in ["color", "black"]:
        raise ValueError("Invalid mode: must be either 'color' or 'black'.")

    package = f"{constants.EMOJIS_DIR}.{mode}.{group}"

    hex_codes = []
    for file in resources.contents(package):
        if file.endswith(".png"):
            # Extract the base name without extension (i.e., without ".png")
            hex_code = os.path.splitext(file)[0]
            hex_codes.append(hex_code)
    hex_codes.sort()

    return hex_codes


def _load_emoji(
        mode: str, group: str, hex_code: str,
        return_pil: bool = False) -> Image.Image | np.ndarray:
    """Load an emoji into memory.

    Args:
        mode (str): The mode of the emoji.  Either "color" or "black".
        group (str): The name of the group of the emoji.
        hex_code (str): The hex code of the emoji to load.
        return_pil (bool): Whether to return a PIL Image (True) or a
            NumPy array (False).  Defaults to False.

    Returns:
        Image.Image or np.ndarray: The loaded emoji image.

    Raises:
        FileNotFoundError: If the specified emoji is not found.
    """
    # Filename of the emoji that we want to load
    file_name = hex_code + ".png"

    try:
        # Open the file using importlib.resources
        with resources.open_binary(
                f"{constants.EMOJIS_DIR}.{mode}.{group}", file_name
        ) as file:
            # Read the file into a bytes object
            data = file.read()

        # Create a BytesIO object from the data, and load the image from the BytesIO object
        data_io = io.BytesIO(data)
        emoji_image = Image.open(data_io)

        # Convert to RGBA mode if necessary
        emoji_image = emoji_image.convert("RGBA") if emoji_image.mode != "RGBA" else emoji_image

        return emoji_image if return_pil else np.array(emoji_image)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Failed to load emoji: {file_name} not found.") from exc


def _rescale_emoji(
        emoji_image: np.ndarray, padding: float,
        return_pil: bool = True) -> Image.Image | np.ndarray:
    """Rescale an emoji so that it fits inside the circle inscribed in a
       square image.

    Args:
        emoji_image (np.ndarray): The emoji image to rescale.
        padding (float): Determines the (relative) amount of padding to
            be used when placing the emoji on a playing card.  Defaults
            to 0.1.
        return_pil (bool): Whether to return a PIL Image (True) or a
            NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The rescaled emoji image.

    Raises:
        ValueError: If the "emoji_image" is not a NumPy array or not a
            square image.
        ValueError: If the "padding" is not in the range of [0, 1).
    """
    # Ensure that the input image is a NumPy array
    if not isinstance(emoji_image, np.ndarray):
        raise ValueError("Emoji image is not a NumPy array.")

    # Ensure that the input image is a square image
    if emoji_image.shape[0] != emoji_image.shape[1]:
        raise ValueError("Input image must be a square array.")

    # Check if padding is within the range of [0, 1)
    if not 0 <= padding < 1:
        raise ValueError("Scale must be in the range of (0, 1].")

    # Determine non-transparent pixels
    non_transparent_px = np.argwhere(emoji_image[:, :, 3] > 0)

    # Transform coordinates so that center pixel corresponds to origin of Euclidean plane
    # NOTE: The y-axis is flipped here, which doesn't matter for computing the Euclidean norm
    radius = emoji_image.shape[0] // 2
    non_transparent_px -= radius

    # Determine the maximum Euclidean norm of all non-transparent pixels
    outermost_px_norm = np.max(np.linalg.norm(non_transparent_px, axis=1))

    # Compute rescaling factor and resulting target size
    target_norm = (1 - padding) * radius
    rescaling_factor = target_norm / outermost_px_norm
    image_size = emoji_image.shape[0]  # size of input image
    target_size = int(image_size * rescaling_factor)  # target size of rescaled image

    # Convert to PIL Image and rescale
    emoji_image_pil = Image.fromarray(emoji_image)
    # pylint: disable=no-member
    emoji_image_pil = emoji_image_pil.resize((target_size, target_size), Image.LANCZOS)

    # Compute offset for centering/cropping the rescaled image
    # NOTE: Taking the absolute value handles both cases (i.e., rescaling_factor < 1 and
    #       rescaling_factor > 1)
    offset = abs(target_size - image_size) // 2

    if rescaling_factor < 1:
        # Paste rescaled (smaller) image onto fully transparent image of original size
        rescaled_image = Image.new("RGBA", (image_size, image_size), (255, 255, 255, 0))
        rescaled_image.paste(emoji_image_pil, (offset, offset), mask=emoji_image_pil)
    elif rescaling_factor > 1:
        # Crop rescaled (larger) image
        rescaled_image = emoji_image_pil.crop(
            (offset, offset, image_size + offset, image_size + offset)
        )
    else:
        # Return original image
        rescaled_image = emoji_image_pil

    return rescaled_image if return_pil else np.array(rescaled_image)


def _place_emoji(
        card_image: Image.Image, emoji_image: Image.Image,
        placement: dict[str, int | np.ndarray | float],
        return_pil: bool = True) -> Image.Image | np.ndarray:
    """Place an emoji on a card image at specified coordinates with the
       specified size

    Args:
        card_image (Image.Image): The card image on which the emoji is
            to be placed.
        emoji_image (Image.Image): The emoji image to be placed on the
            card image.
        placement (dict[str, int | np.ndarray | float]): A
            dictionary containing the placement information.  The
            dictionary must contain the following keys:
                - "size" (int): The size of the emoji in pixels.
                - "center" (np.ndarray): The coordinates of the center
                    of the emoji on the image.
                - "rotation" (float): The rotation angle of the emoji in
                    degrees.  Must be in the range [0, 360).
        return_pil (bool): Whether to return a PIL Image (True) or a
            NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The image w/ the emoji placed on it.

    Raises:
        ValueError: If the "rotation_angle" is provided but is outside
            the valid range [0, 360).
    """
    # Calculate the top-left coordinates of the emoji based on the center coordinates and size
    top_left = tuple(placement["center"] - placement["size"] // 2)

    # Resize the emoji to the specified size
    emoji_image = emoji_image.resize((placement["size"], placement["size"]))

    # Check the rotation angle and rotate the emoji
    if 0 <= placement["rotation"] < 360:
        emoji_image = emoji_image.rotate(placement["rotation"])
    else:
        raise ValueError("Invalid rotation angle: must be in the range [0, 360).")

    # Paste the emoji onto the original image at the specified coordinates
    # noinspection PyTypeChecker
    card_image.paste(emoji_image, top_left, mask=emoji_image)

    return card_image if return_pil else np.array(card_image)


def create_dobble_card(
        emojis: list[dict[str, str]] = None,
        card_params: dict[str, int | str | float] = None,
        return_pil: bool = True) -> Image.Image | np.ndarray:
    """Create a single Dobble playing card.

    Args:
        emojis (list[dict[str, str]]): The list of emojis to be placed
            on the playing card.  Each emoji is specified by a
            dictionary which must contain the following keys:
                - "mode" (str): The mode of the emoji.  Either "color"
                    or "black".
                - "group" (str): The name of the group of the emoji.
                - "hex" (str): The hex code of the emoji to load.
            If not provided, a random number of emojis similar to the
            ones used in the original Dobble deck are used.
        card_params (dict[str, str | int]): A dictionary containing the
            parameters of the playing card.  The dictionary must contain
            the following keys:
                - "size" (int): The size of the playing card in pixels.
                    Defaults to 1024.
                - "packing" (str): The type of circle packing used to
                    arrange the emojis on the playing card.  Chosen
                    randomly, if not provided.  Defaults to None.
                - "padding" (float): Determines the (relative) amount of
                    padding to be used when placing the emojis on the
                    playing card.  Defaults to 0.1.
        return_pil (bool): Whether to return a PIL Image (True) or a
            NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The generated image of a Dobble
            playing card.
    """
    # Retrieve a random subset of the emojis resembling the symbols in a classic Dobble deck if no
    # emojis were provided
    # NOTE: For all but one type of packing ("cci"), packings are only provided for n >= 5 circles.
    #       Hence, we choose a random number of emojis in the range [5, 8] to ensure that we can
    #       always create a Dobble card.
    if emojis is None:
        emojis = random.sample(constants.CLASSIC_DOBBLE_EMOJIS, random.randint(5, 8))

    # Retrieve the default card parameters if none were provided
    if card_params is None:
        card_params = constants.DEFAULT_CARD_PARAMS.copy()

    # Set the default size of the card if none was provided
    if "size" not in card_params or card_params["size"] is None:
        card_params["size"] = constants.DEFAULT_CARD_PARAMS["size"]

    # Choose a random packing type if none was provided
    if "packing" not in card_params or card_params["packing"] is None:
        card_params["packing"] = random.choice(list(constants.PACKING_TYPES_DICT.keys()))

    # Set the default scale if none was provided
    if "padding" not in card_params or card_params["padding"] is None:
        card_params["padding"] = constants.DEFAULT_CARD_PARAMS["padding"]

    # Get packing data
    packing_data = packing.get_packing_data(
        len(emojis), card_params["packing"], card_params["size"]
    )

    # Create empty card
    dobble_card = _create_empty_card(card_params["size"])

    # Place emojis on card one-by-one
    for count, emoji in enumerate(emojis):
        # Load and rescale the emoji
        emoji_image = _rescale_emoji(
            _load_emoji(emoji["mode"], emoji["group"], emoji["hex"]),
            card_params["padding"]
        )
        # Gather information about the placement of the emoji
        placement = {
            "size": packing_data["radii"][count],
            "center": packing_data["coordinates"][count],
            "rotation": random.randint(0, 359)
        }
        # Place the emoji on the card
        dobble_card = _place_emoji(dobble_card, emoji_image, placement)

    return dobble_card if return_pil else np.array(dobble_card)


def create_dobble_deck(
        emojis: list[dict[str, str]] = None,
        deck_params: dict[str, str | int] = None,
        card_params: dict[str, int | str | float] = None) -> dict[str, str]:
    """Create a full deck of Dobble playing cards (i.e., generate images
       and save to disk).

    Args:
        emojis (list[dict[str, str]]): The list of emojis to be used for
            the deck.  Each emoji is specified by a dictionary which
            must contain the following keys:
                - "mode" (str): The mode of the emoji.  Either "color"
                    or "black".
                - "group" (str): The name of the group of the emoji.
                - "hex" (str): The hex code of the emoji to load.
            If not provided, emojis similar to the ones used in the
            original Dobble deck are used.
        deck_params (dict[str, str | int]): A dictionary containing the
            parameters of the deck. The dictionary must contain the
            following keys:
                - "name" (str): The name of the deck.  This will be used
                    to create the directory in which all the images are
                    stored.  Defaults to "my-dobble-deck".
                - "emojis_per_card" (int): The number of emojis to place
                    on each card.  Must be one more than some prime
                    power, i.e., "emojis_per_card" = p^k + 1, with p
                    prime.  Defaults to 8.
                - "save_dir" (str): The directory in which to save the
                    generated images.  If not provided, the images are
                    saved in the current working directory.  Defaults to
                    None.
        card_params (dict[str, str | int]): A dictionary containing the
            parameters of the playing card. The dictionary must contain
            the following keys:
                - "size" (int): The size of the playing card in pixels.
                    Defaults to 1024.
                - "packing" (str): The type of circle packing used to
                    arrange the emojis on the playing card.  Chosen
                    randomly, if not provided.  Defaults to None.
                - "padding" (float): Determines the (relative) amount of
                    padding to be used when placing the emojis on the
                    playing cards.  Defaults to 0.1.

    Returns:
        dict[str, str]: A dictionary containing the file paths to the
            generated CSV files that store all information about the
            playing cards ("deck") and the emoji labels ("emojis").
    """
    # Retrieve the emojis resembling the symbols in a classic Dobble deck if none were provided
    if emojis is None:
        emojis = constants.CLASSIC_DOBBLE_EMOJIS.copy()

    # Retrieve the default deck parameters if none were provided
    if deck_params is None:
        deck_params = constants.DEFAULT_DECK_PARAMS.copy()

    # Set the default name of the deck if none was provided
    if "name" not in deck_params or deck_params["name"] is None:
        deck_params["name"] = constants.DEFAULT_DECK_PARAMS["name"]

    # Set the default number of emojis per card if none was provided
    if "emojis_per_card" not in deck_params or deck_params["emojis_per_card"] is None:
        deck_params["emojis_per_card"] = constants.DEFAULT_DECK_PARAMS["emojis_per_card"]

    # Construct the path to the directory in which to save the images
    if "save_dir" not in deck_params or deck_params["save_dir"] is None:
        # If no "save_dir" was provided, save the images in the current working directory
        deck_dir = os.path.join(os.getcwd(), deck_params["name"])
    else:
        # If a "save_dir" was provided, check if it exists and is a directory
        if os.path.isdir(deck_params["save_dir"]):
            deck_dir = os.path.join(deck_params["save_dir"], deck_params["name"])
        else:
            raise ValueError(
                f"Invalid 'save_dir': '{deck_params['save_dir']}' does not exist"
                f"or is not a directory."
            )

    # If the "deck_dir" already exists, abort the function and inform the user
    if os.path.exists(deck_dir):
        raise ValueError(
            f"Invalid 'deck_name': '{deck_params['name']}' already exists in the specified"
            f"'save_dir'."
        )

    # NOTE: We do not create the directory right away because we want to make sure that the number
    #       of emojis provided is sufficient to create the deck.  If not, we raise an error and do
    #       not create the directory.

    # Compute number of cards in the deck
    # NOTE: Remember that there are as many distinct emojis in a deck as there are playing cards,
    #       and that the number of playing cards in a deck is given by n^2 + n + 1, with
    #       n + 1 = deck_params["emojis_per_card"]
    num_cards = (deck_params["emojis_per_card"] - 1) ** 2 + deck_params["emojis_per_card"]

    # Check whether the appropriate number of emojis was provided
    if len(emojis) < num_cards:
        raise ValueError("Not enough emojis provided to create the Dobble deck.")
    if len(emojis) > num_cards:
        # If there are more emojis than we need, we randomly choose a subset of the appropriate
        # size and raise a warning to inform the user
        emojis = random.sample(emojis, num_cards)
        print(
            f"WARNING: More emojis provided than needed."
            f"Randomly choosing a subset of {num_cards} emojis."
        )

    # Extract the hex codes of all emojis used to create the deck
    hex_codes = [emoji["hex"] for emoji in emojis]

    # Create the directories in which to store the images and CSV files.  The CSV files are stored
    # in a subdirectory called "info".  The CSV files contain information about the individual
    # cards (i.e., which emojis are placed on which card) and the emojis themselves (i.e., the hex
    # code of each emoji and its corresponding label).
    os.makedirs(deck_dir)
    os.makedirs(os.path.join(deck_dir, "info"))

    # Create the filepaths pointing to the CSV files
    csv_files = {
        "deck": os.path.join(deck_dir, "info", "deck.csv"),
        "emojis": os.path.join(deck_dir, "info", "emojis.csv")
    }

    # Create a CSV file containing the hex code of each emoji along with a counter from 1 to
    # "len(hex_codes)" that serves as the emoji label
    emojis_info = pd.DataFrame({"Hex": hex_codes, "Label": range(1, len(hex_codes) + 1)})
    emojis_info.to_csv(csv_files["emojis"], index=False)

    # Set up a CSV file to store information about the individual cards
    with open(csv_files["deck"], "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["FilePath"] + ["Emoji" + str(i + 1) for i in range(deck_params["emojis_per_card"])]
        )

    # Compute incidence matrix of corresponding finite projective plane.  This determines which
    # emojis are placed on which cards.
    # NOTE: The number of emojis per card has to be one more than some prime power, i.e.,
    #       "emojis_per_card" = p^k + 1, with p prime.  Otherwise, the incidence matrix cannot be
    #       computed and an error is raised.
    incidence_matrix = utils.compute_incidence_matrix(deck_params["emojis_per_card"] - 1)

    # Create playing cards one-by-one using the incidence matrix to decide which emojis to put on
    # which card
    # NOTE: len(a) is equivalent to np.shape(a)[0] for N-D arrays with N>=1.
    for card in range(num_cards):
        # Find the emojis that are to be placed on the playing card currently being created
        which_emojis = [emojis[idx] for idx in np.nonzero(incidence_matrix[card])[0]]
        random.shuffle(which_emojis)

        # Create playing card and save in directory
        dobble_card = create_dobble_card(which_emojis, card_params)
        file_path = os.path.join(deck_dir, f"{deck_params['name']}_{card + 1:03d}.png")
        dobble_card.save(file_path)

        # Write card information to the CSV file
        with open(csv_files["deck"], "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([file_path] + [emoji["hex"] for emoji in which_emojis])

    return csv_files
