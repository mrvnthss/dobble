"""Functionality to load circle packing data.

This module provides functions to read circle packing data from files,
and convert relative coordinates and relative radii to integer values
(number of pixels) for use in images.

Functions:
    _read_coordinates_from_file: Read coordinates of a specified circle
      packing from a text file.
    _read_radius_from_file: Read the radius of the largest circle of a
      specified circle packing from a text file.
    _compute_radii: Compute the radii of all circles in a packing.
    _convert_coordinates_to_pixels: Convert relative coordinates to
      pixel coordinates.
    _convert_radii_to_pixels: Convert relative radii to number of
      pixels.
    get_packing_data: Get data (coordinates and radii) of a specified
      packing in pixel values.
"""


from importlib.resources import files

import numpy as np

from . import constants
from . import utils


def _read_coordinates_from_file(
        num_circles: int,
        packing: str
) -> np.ndarray:
    """Read coordinates of a specified circle packing from a text file.

    Args:
        num_circles: Number of circles in the packing.
        packing: Type of circle packing.

    Returns:
        The coordinates of the circles in the packing as an (n x 2)
          array, where n = num_circles.

    Raises:
        ValueError: If the packing is not one of the supported packings
          or if the number of circles is not a positive integer.
        FileNotFoundError: If the text file for the specified packing
          type and number of circles is not found.
    """

    # Check if the number of circles is a positive integer
    if not utils.is_integer(num_circles) or num_circles < 1:
        raise ValueError("Number of circles must be a positive integer.")

    # Check if a valid packing is provided
    if not utils.is_valid_packing(packing):
        raise ValueError(f"Invalid packing: '{packing}' is not supported.")

    # Construct the file name based on the packing type and number of circles
    packing = packing.lower()
    file_name = packing + str(int(num_circles)) + ".txt"

    try:
        fpath = files(constants.PACKINGS_DIR) / packing / file_name
        with fpath.open("r") as file:
            # Read the text file line by line
            lines = file.readlines()
            # Strip extra spaces from each line and split into columns
            data = [line.strip().split() for line in lines]
            # Convert the data to a NumPy array and skip the first column
            data = np.array(data)[:, 1:3].astype(float)
        return data
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Coordinates file for '{packing}' packing with {num_circles} circles not found."
        ) from exc


def _read_radius_from_file(
        num_circles: int,
        packing: str
) -> float:
    """Return the radius of the largest circle of a packing.

    Args:
        num_circles: Number of circles in the packing.
        packing: Type of circle packing.

    Returns:
        The radius of the largest circle of the specified packing.

    Raises:
        ValueError: If either the packing or the number of circles are
          invalid, or if no radius is found for the specified
          combination of packing type and number of circles.
    """

    # Check if the number of circles is a positive integer
    if not utils.is_integer(num_circles) or num_circles < 1:
        raise ValueError("Number of circles must be a positive integer.")

    # Check if a valid packing is provided
    if not utils.is_valid_packing(packing):
        raise ValueError(f"Invalid packing: '{packing}' is not supported.")

    packing = packing.lower()
    file_name = constants.RADIUS_FILE

    fpath = files(constants.PACKINGS_DIR) / packing / file_name
    with fpath.open("r") as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 2 and int(values[0]) == num_circles:
                return float(values[1])
    raise ValueError(
        f"No radius found for packing '{packing}' with {int(num_circles)} circles."
    )


def _compute_radii(
        num_circles: int,
        packing: str,
        largest_radius: float
) -> np.ndarray:
    """Compute the radii of all circles in a packing.

    Args:
        num_circles: Total number of circles in the packing.
        packing: Type of circle packing.
        largest_radius: Radius of the largest circle in the packing.
          Must be in the range (0, 1].

    Returns:
        The computed radii of all the circles in the packing.

    Raises:
        ValueError: If the packing is not one of the supported packings
          or if the number of circles is not a positive integer.
    """

    # Check if the number of circles is a positive integer
    if not utils.is_integer(num_circles) or num_circles < 1:
        raise ValueError("Number of circles must be a positive integer.")

    # Check if a valid packing is provided
    if not utils.is_valid_packing(packing):
        raise ValueError(f"Invalid packing: '{packing}' is not supported.")

    # Check if the largest radius is within the range (0, 1]
    if not 0 < largest_radius <= 1:
        raise ValueError("Largest radius must be in the range (0, 1].")

    packing = packing.lower()
    radius_function = constants.PACKINGS_DICT[packing][0]
    function_values = np.sort(
        np.array([radius_function(n + 1) for n in range(int(num_circles))])
    )

    ratio = largest_radius / function_values[-1]
    radii = function_values * ratio

    return radii


def _convert_coordinates_to_pixels(
        rel_coordinates: np.ndarray,
        img_size: int
) -> np.ndarray:
    """Convert relative coordinates to pixel coordinates.

    The function takes relative coordinates in the range [-1, 1] and
    converts them to pixel coordinates based on the size of a square
    image.  The relative coordinates are assumed to be in normalized
    form, where the origin (0, 0) corresponds to the center of the image
    and the values (-1, -1) and (1, 1) correspond to the lower left and
    upper right corner of the image, respectively.

    Args:
        rel_coordinates: Relative coordinates in the range [-1, 1].
        img_size: Size of the square image that coordinates are to be
          based on.

    Returns:
        Pixel coordinates corresponding to the relative coordinates.

    Raises:
        ValueError: If the relative coordinates are outside the range
          [-1, 1] or if the image size is not a positive integer.
    """

    # Check if the relative coordinates are within the range [-1, 1]
    if not np.logical_and(-1 <= rel_coordinates, rel_coordinates <= 1).all():
        raise ValueError("All relative coordinates must be in the range [-1, 1].")

    # Check if the image size is a positive integer
    if not utils.is_integer(img_size) or img_size < 1:
        raise ValueError(f"Image size must be a positive integer, got {img_size}.")

    # Shift coordinates from [-1, 1] to [0, 1]
    rel_coordinates = rel_coordinates / 2 + 0.5

    # Scale coordinates from [0, 1] to [0, img_size] and convert to integer values
    coordinates = np.floor(rel_coordinates * img_size).astype("int")

    return coordinates


def _convert_radii_to_pixels(
        rel_radii: np.ndarray,
        img_size: int
) -> np.ndarray:
    """Convert relative radii to number of pixels.

    Args:
        rel_radii: Relative radii in the range (0, 1].
        img_size: Size of the square image that radii are to be based
          on.

    Returns:
        Number of pixels corresponding to the relative radii.

    Raises:
        ValueError: If any relative radius is outside the valid range
          (0, 1] or if the image size is not a positive integer.
    """

    # Check if all relative radii are within the range (0, 1]
    if not np.logical_and(0 < rel_radii, rel_radii <= 1).all():
        raise ValueError("All relative radii must be in the range (0, 1].")

    # Check if the image size is a positive integer
    if not utils.is_integer(img_size) or img_size < 1:
        raise ValueError(f"Image size must be a positive integer, got {img_size}.")

    radii = np.floor(rel_radii * img_size).astype("int")

    return radii


def get_packing_data(
        num_circles: int,
        packing: str,
        img_size: int
) -> dict[str, np.ndarray]:
    """Get data (coordinates and radii) of a packing in pixel values.

    Args:
        num_circles: Total number of circles in the packing.
        packing: Type of circle packing.
        img_size: Size of the square image that coordinates and radii
          are to be based on.

    Returns:
        A dictionary containing the coordinates and radii in pixel
          values.
    """

    # Get coordinates
    coordinates = _convert_coordinates_to_pixels(
        _read_coordinates_from_file(num_circles, packing), img_size
    )

    # Get radii (i.e., sizes of the circles in pixels)
    largest_radius = _read_radius_from_file(num_circles, packing)
    radii = _convert_radii_to_pixels(
        _compute_radii(num_circles, packing, largest_radius),
        img_size
    )

    # Combine into dictionary
    packing_data = {
        "coordinates": coordinates,
        "radii": radii
    }

    return packing_data
