"""Module for creating custom Dobble playing cards and decks.

This module contains functions to create individual Dobble playing cards and full decks of Dobble playing cards.

Functions:
    - _create_empty_card: Create a square image of a white disk against a transparent background.
    - _get_hexcodes: Retrieve the hexcodes of all emojis in a specified group.
    - _load_emoji: Load a specified emoji into memory.
    - _rescale_emoji: Rescale an emoji so that it fits inside the circle inscribed in a square image.
    - _place_emoji: Place an emoji on a given image at specified coordinates with the specified size.
    - create_dobble_card: Create a single Dobble playing card.
    - create_dobble_deck: Create a full deck of Dobble playing cards.

The module uses the 'packing' and 'utils' modules from the 'dobble' package to arrange the emojis on the cards and to
compute the incidence matrices for finite projective planes to distribute the emojis across the playing cards,
respectively.
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
    """Create a square image of a white disk against a transparent background.

    Args:
        image_size (int): The size of the square image in pixels.
        return_pil (bool): Whether to return a PIL Image (True) or a NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The generated image of a white disk against a transparent background.
    """
    # Create a new transparent image with RGBA mode
    image = Image.new('RGBA', (image_size, image_size), (0, 0, 0, 0))

    # Create a new draw object and draw a white disk onto the image
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, image_size, image_size), fill=(255, 255, 255, 255))

    return image if return_pil else np.array(image)


def _get_hexcodes(mode: str, group: str) -> list[str]:
    """Retrieve the hexcodes of all emojis in a specified group.

    Args:
        mode (str): The mode of the emojis.  Either 'color' or 'black'.
        group (str): The name of the group of emojis.

    Returns:
        list[str]: A list of hexcodes of all emojis of the specified mode in the specified group.
    """
    # Ensure that the specified mode is valid
    if mode not in ['color', 'black']:
        raise ValueError("Invalid mode: must be either 'color' or 'black'.")

    package = f'{constants.EMOJIS_DIR}.{mode}.{group}'

    hexcodes = []
    for file in resources.contents(package):
        if file.endswith('.png'):
            # Extract the base name without extension (i.e., without '.png')
            hexcode = os.path.splitext(file)[0]
            hexcodes.append(hexcode)
    hexcodes.sort()

    return hexcodes


def _load_emoji(mode: str, group: str, hexcode: str, return_pil: bool = False) -> Image.Image | np.ndarray:
    """Load a specified emoji into memory.

    Args:
        mode (str): The mode of the emojis.  Either 'color' or 'black'.
        group (str): The name of the group of emojis to use.
        hexcode (str): The hexcode of the emoji to load.
        return_pil (bool): Whether to return a PIL Image (True) or a NumPy array (False).  Defaults to False.

    Returns:
        Image.Image or np.ndarray: The loaded emoji image.

    Raises:
        FileNotFoundError: If the specified emoji is not found.
    """
    # Filename of the emoji that we want to load
    file_name = hexcode + '.png'

    try:
        # Open the file using importlib.resources
        with resources.open_binary(f'{constants.EMOJIS_DIR}.{mode}.{group}', file_name) as file:
            # Read the file into a bytes object
            data = file.read()

        # Create a BytesIO object from the data, and load the image from the BytesIO object
        data_io = io.BytesIO(data)
        emoji_image = Image.open(data_io)

        # Convert to RGBA mode if necessary
        emoji_image = emoji_image.convert('RGBA') if emoji_image.mode != 'RGBA' else emoji_image

        return emoji_image if return_pil else np.array(emoji_image)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Failed to load emoji: {file_name} not found.") from exc


def _rescale_emoji(emoji_image: np.ndarray, scale: float, return_pil: bool = True) -> Image.Image | np.ndarray:
    """Rescale an emoji so that it fits inside the circle inscribed in a square image.

    Args:
        emoji_image (np.ndarray): The emoji image to rescale as a NumPy array.
        scale (float): Determines to what extent the emoji should fill the inscribed circle.
        return_pil (bool): Whether to return a PIL Image (True) or a NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The rescaled emoji image.

    Raises:
        ValueError: If the 'emoji_image' is not a NumPy array or not a square image.
        ValueError: If the 'scale' is not in the range of (0, 1].
    """
    # Ensure that the input image is a NumPy array
    if not isinstance(emoji_image, np.ndarray):
        raise ValueError("Emoji image is not a NumPy array.")

    # Ensure that the input image is a square image
    if emoji_image.shape[0] != emoji_image.shape[1]:
        raise ValueError('Input image must be a square array.')

    # Check if scale is within the range of (0, 1]
    if not 0 < scale <= 1:
        raise ValueError('Scale must be in the range of (0, 1].')

    # Determine non-transparent pixels
    non_transparent_px = np.argwhere(emoji_image[:, :, 3] > 0)

    # Transform coordinates so that center pixel corresponds to origin of Euclidean plane
    # NOTE: The y-axis is flipped here, which doesn't matter for computing the Euclidean norm
    radius = emoji_image.shape[0] // 2
    non_transparent_px -= radius

    # Determine the maximum Euclidean norm of all non-transparent pixels
    outermost_px_norm = np.max(np.linalg.norm(non_transparent_px, axis=1))

    # Compute rescaling factor and resulting target size
    target_norm = scale * radius
    rescaling_factor = target_norm / outermost_px_norm
    image_size = emoji_image.shape[0]  # size of input image
    target_size = int(image_size * rescaling_factor)  # target size of rescaled image

    # Convert to PIL Image and rescale
    emoji_image_pil = Image.fromarray(emoji_image)
    # pylint: disable=no-member
    emoji_image_pil = emoji_image_pil.resize((target_size, target_size), Image.LANCZOS)

    # Compute offset for centering/cropping the rescaled image
    # NOTE: Taking the absolute value handles both cases (i.e., rescaling_factor < 1 and rescaling_factor > 1)
    offset = abs(target_size - image_size) // 2

    if rescaling_factor < 1:
        # Paste rescaled (smaller) image onto fully transparent image of original size
        rescaled_image = Image.new('RGBA', (image_size, image_size), (255, 255, 255, 0))
        rescaled_image.paste(emoji_image_pil, (offset, offset), mask=emoji_image_pil)
    elif rescaling_factor > 1:
        # Compute coordinates for cropping
        left = offset
        top = offset
        right = left + image_size
        bottom = top + image_size

        # Crop rescaled (larger) image
        rescaled_image = emoji_image_pil.crop((left, top, right, bottom))
    else:
        # Return original image
        rescaled_image = emoji_image_pil

    return rescaled_image if return_pil else np.array(rescaled_image)


def _place_emoji(image: Image.Image, emoji_image: Image.Image, emoji_size: int, emoji_center: tuple[int, int],
                 rotation_angle: float = None, return_pil: bool = True) -> Image.Image | np.ndarray:
    """Place an emoji on a given image at specified coordinates with the specified size.

    Args:
        image (Image.Image): The image on which the emoji is to be placed.
        emoji_image (Image.Image): The emoji image to be placed on the image.
        emoji_size (int): The desired size of the emoji in pixels when placed on the image.
        emoji_center (tuple[int, int]): The coordinates of the center of the emoji in the form (x, y).
        rotation_angle (float): The angle (in degrees) by which to rotate the emoji.  Defaults to None.
        return_pil (bool): Whether to return a PIL Image (True) or a NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The image with the emoji placed on it.

    Raises:
        ValueError: If the 'rotation_angle' is provided but is outside the valid range [0, 360).
    """
    x_center, y_center = emoji_center

    # Calculate the top-left coordinates of the emoji based on the center coordinates and size
    x_left = x_center - emoji_size // 2
    y_top = y_center - emoji_size // 2

    # Resize the emoji to the specified size
    emoji_image = emoji_image.resize((emoji_size, emoji_size))

    # Rotate the emoji if a rotation angle is provided
    if rotation_angle:
        if 0 <= rotation_angle < 360:
            emoji_image = emoji_image.rotate(rotation_angle)
        else:
            raise ValueError('Invalid rotation angle: must be in the range [0, 360).')

    # Paste the emoji onto the original image at the specified coordinates
    image.paste(emoji_image, (x_left, y_top), mask=emoji_image)

    return image if return_pil else np.array(image)


def create_dobble_card(emojis: list[dict[str, str]], packing_type: str = 'ccir', image_size: int = 1024,
                       scale: float = 0.9, return_pil: bool = True) -> Image.Image | np.ndarray:
    """Create a single Dobble playing card.

    Args:
        emojis (list[dict[str, str]]): The list of emojis to be placed on the playing card.  Each list entry is a
            dictionary specifying the mode, group, and hexcode of the emoji to be used.
        packing_type (str): The type of circle packing used to arrange the emojis on the playing card.
            Defaults to 'ccir'.
        image_size (int): The size of the square image in pixels.  Defaults to 1024.
        scale (float): Determines to what extent the emoji should fill the inscribed circle.  Defaults to 0.9.
        return_pil (bool): Whether to return a PIL Image (True) or a NumPy array (False).  Defaults to True.

    Returns:
        Image.Image or np.ndarray: The generated image of a Dobble playing card.
    """
    dobble_card = _create_empty_card(image_size)
    num_emojis = len(emojis)
    packing_data = packing.get_packing_data(num_emojis, packing_type, image_size)

    # Place emojis on card
    for count, emoji in enumerate(emojis):
        emoji_dict = {
            'image': _rescale_emoji(_load_emoji(emoji['mode'], emoji['group'], emoji['hexcode']), scale),
            'size': packing_data['sizes'][count],
            'center': packing_data['coordinates'][count],
            'rotation_angle': random.randint(0, 359)
        }

        dobble_card = _place_emoji(dobble_card, **emoji_dict)

    return dobble_card if return_pil else np.array(dobble_card)


def create_dobble_deck(
        deck_name: str, emojis: list[dict[str, str]], emojis_per_card: int, save_dir: str = None,
        packing_type: str = None, image_size: int = 1024, scale: float = 0.9) -> tuple[str, str]:
    """Create a full deck of Dobble playing cards (i.e., generate and save images).

    Args:
        deck_name (str): The name of the deck.  This will be used to create the directory in which all the images
            are stored.
        emojis (list[dict[str, str]]): The list of emojis to be used for the deck of playing cards.  Each list entry is
            a dictionary specifying the mode, group, and hexcode of the emoji to be used.
        emojis_per_card (int): The number of emojis to place on each card.
        save_dir (str): The directory in which to save the generated images.  If not provided, the images are saved in
            the current working directory.  Defaults to None.
        packing_type (str): The type of circle packing used to arrange the emojis on the playing cards. If not provided,
            a packing type is randomly chosen for each card.  Defaults to None.
        image_size (int): The size of the square image in pixels.  Defaults to 1024.
        scale (float): Determines to what extent the emoji should fill the inscribed circle.  Defaults to 0.9.

    Returns:
        tuple[str, str]: A tuple containing the file paths to the generated CSV files that store all
            information about the playing cards ('deck.csv') as well as the emoji labels ('emoji_labels.csv').
    """
    # Construct the path to the directory in which to save the images
    if save_dir is not None:
        # Check if the specified 'save_dir' exists
        if os.path.isdir(save_dir):
            deck_dir = os.path.join(save_dir, deck_name)
        else:
            raise ValueError(f"Invalid 'save_dir': '{save_dir}' does not exist or is not a directory.")
    else:
        # If no 'save_dir' was provided, save the images in the current working directory
        deck_dir = os.path.join(os.getcwd(), deck_name)

    # If the 'deck_dir' already exists, abort the function and inform the user
    if os.path.exists(deck_dir):
        raise ValueError(f"Invalid 'deck_name': '{deck_name}' already exists in the specified 'save_dir'.")

    # NOTE: We do not create the directory right away because we want to make sure that the number of emojis provided
    #       is sufficient to create the deck.  If not, we raise an error and do not create the directory.

    # Compute number of cards in the deck
    # NOTE: Remember that there are as many distinct emojis in a deck as there are playing cards, and that the number of
    #       playing cards in a deck is given by n^2 + n + 1, with n + 1 = 'emojis_per_card'
    order = emojis_per_card - 1
    num_cards = order ** 2 + order + 1

    # Check whether the appropriate number of emojis was provided
    num_emojis_provided = len(emojis)
    if num_emojis_provided < num_cards:
        raise ValueError('Not enough emojis provided to create the Dobble deck.')
    if num_emojis_provided > num_cards:
        # If there are more emojis than we need, we randomly choose a subset of the appropriate size and raise a warning
        # to inform the user
        emojis = random.sample(emojis, num_cards)
        print(f'WARNING: More emojis provided than needed.  Randomly choosing a subset of {num_cards} emojis.')

    # Create the directories in which to store the images and CSV files.  The CSV files are stored in a subdirectory
    # called 'info'.  The CSV files contain information about the individual cards (i.e., which emojis are placed on
    # which card) and the emojis (i.e., the hexcode of each emoji and its corresponding label).
    csv_dir = os.path.join(deck_dir, 'info')
    os.makedirs(deck_dir)
    os.makedirs(csv_dir)

    # Extract the hexcodes of all emojis used to create the deck
    hexcodes = [emoji['hexcode'] for emoji in emojis]

    # Create a CSV file containing the hexcode of each emoji along with a counter from 1 to 'len(emojis)' that serves as
    # the emoji label
    emojis_info = pd.DataFrame({'Hexcode': hexcodes, 'Label': range(1, len(hexcodes) + 1)})
    emojis_csv = os.path.join(csv_dir, 'emojis.csv')
    emojis_info.to_csv(emojis_csv, index=False)

    # Set up a CSV file to store information about the individual cards
    deck_csv = os.path.join(csv_dir, 'deck.csv')
    with open(deck_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['FilePath'] + ['PackingType'] + ['Emoji' + str(i + 1) for i in range(emojis_per_card)]
        )

    # Compute incidence matrix of corresponding finite projective plane.  This determines which emojis are placed on
    # which cards.
    incidence_matrix = utils.compute_incidence_matrix(order)

    # If no 'packing_type' was provided, choose one randomly each time from the 'PACKING_TYPES_DICT' dictionary
    choose_randomly = packing_type is None

    # Create playing cards one-by-one using the incidence matrix to decide which emojis to put on which card
    # NOTE: len(a) is equivalent to np.shape(a)[0] for N-D arrays with N>=1.
    for card in range(num_cards):
        # Find the emojis that are to be placed on the playing card currently being created
        which_emojis = np.where(incidence_matrix[card])[0]
        chosen_emojis = [emojis[idx] for idx in which_emojis]
        random.shuffle(chosen_emojis)

        # If no 'packing_type' was provided initially, choose one randomly from the 'PACKING_TYPES_DICT' dictionary
        if choose_randomly:
            packing_type = random.choice(list(constants.PACKING_TYPES_DICT.keys()))

        # Create playing card and save in directory
        dobble_card = create_dobble_card(chosen_emojis, packing_type, image_size, scale)
        file_name = f'{deck_name}_{card + 1:03d}.png'
        file_path = os.path.join(deck_dir, file_name)
        dobble_card.save(file_path)

        # Write card information to the CSV file
        with open(deck_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([file_path] + [packing_type] + [emoji['hexcode'] for emoji in chosen_emojis])

    return deck_csv, emojis_csv
