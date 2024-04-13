"""Utility functions for handling circle packing data.

This module provides functions to read circle packing data from files,
and convert relative coordinates to pixel values for rendering images.

Functions:
    - _read_coordinates_from_file: Read coordinates of a specified
        circle packing from a text file.
    - _read_radius_from_file: Read the radius of the largest circle of a
        specified circle packing from a text file.
    - _compute_radii: Compute the radii of all circles in a packing.
    - _convert_coordinates_to_pixels: Convert relative coordinates to
        pixel values.
    - _convert_radii_to_pixels: Convert relative radii to pixel values
        based on the size of a square image.
    - get_packing_data: Get data (coordinates and radii) of a specified
        packing in pixel values.

The module uses the "constants" module from the "dobble" package to
access the project-level constants, and in particular, the paths to the
packing data files.
"""

# Standard Library Imports
from importlib import resources

# Third-Party Library Imports
import numpy as np

# Local Imports
from . import constants


def _is_valid_packing_type(packing_type: str) -> bool:
    """Check if the provided packing type is valid.

    Args:
        packing_type (str): Type of circle packing.

    Returns:
        bool: True if the packing type is valid, False otherwise.
    """
    is_str = isinstance(packing_type, str)
    packing_type_exists = packing_type.lower() in constants.PACKING_TYPES_DICT
    is_valid_packing_type = is_str and packing_type_exists

    return is_valid_packing_type


def _read_coordinates_from_file(
        num_circles: int,
        packing_type: str
) -> np.ndarray:
    """Read coordinates of a specified circle packing from a text file.

    Args:
        num_circles (int): Number of circles in the packing.
        packing_type (str): Type of circle packing.

    Returns:
        np.ndarray: The coordinates of the circles in the packing as an
            (n x 2)-array, where n = "num_circles".

    Raises:
        ValueError: If the packing type is not one of the supported
            packing types or if the number of circles is not a positive
            integer.
        FileNotFoundError: If the text file for the specified packing
            type and number of circles is not found.
    """
    # Check if a valid packing type is provided
    if not _is_valid_packing_type(packing_type):
        raise ValueError(f"Invalid packing type: '{packing_type}' is not supported.")

    # Check if the number of circles is a positive integer
    if not isinstance(num_circles, int) or num_circles < 1:
        raise ValueError("Number of circles must be a positive integer.")

    # Construct the file name based on the packing type and number of circles
    packing_type = packing_type.lower()
    file_name = packing_type + str(num_circles) + ".txt"

    try:
        with resources.open_text(f"{constants.PACKING_DIR}.{packing_type}", file_name) as file:
            # Read the text file line by line
            lines = file.readlines()
            # Strip extra spaces from each line and split into columns
            data = [line.strip().split() for line in lines]
            # Convert the data to a NumPy array and skip the first column
            data = np.array(data)[:, 1:3].astype(float)
        return data
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Coordinates file for '{packing_type}' packing with {num_circles} circles not found."
        ) from exc


def _read_radius_from_file(
        num_circles: int,
        packing_type: str
) -> float:
    """Read the radius of the largest circle of a specified circle
       packing from a text file.

    Args:
        num_circles (int): Number of circles in the packing.
        packing_type (str): Type of circle packing.

    Returns:
        float: The radius of the largest circle of the packing.

    Raises:
        ValueError: If either the packing type or the number of circles
            are invalid, or if no radius is found for the specified
            combination of packing type and number of circles.
        FileNotFoundError: If the text file for the specified packing
            type is not found.
    """
    # Check if a valid packing type is provided
    if not _is_valid_packing_type(packing_type):
        raise ValueError(f"Invalid packing type: '{packing_type}' is not supported.")

    # Check if the number of circles is a positive integer
    if not isinstance(num_circles, int) or num_circles < 1:
        raise ValueError("Number of circles must be a positive integer.")

    packing_type = packing_type.lower()
    file_name = constants.RADIUS_TXT

    try:
        with resources.open_text(f"{constants.PACKING_DIR}.{packing_type}", file_name) as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 2 and int(values[0]) == num_circles:
                    return float(values[1])
        raise ValueError(
            f"No radius found for packing type '{packing_type}' with {num_circles} circles."
        )
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Radius file for '{packing_type}' packing not found.") from exc


def _compute_radii(
        num_circles: int,
        packing_type: str,
        largest_radius: float
) -> np.ndarray:
    """Compute the radii of all circles in a packing.

    Args:
        num_circles (int): Total number of circles in the packing.
        packing_type (str): Type of circle packing.
        largest_radius (float): Radius of the largest circle in the
            packing.

    Returns:
        np.ndarray: The computed radii of the circles in the packing.

    Raises:
        ValueError: If the packing type is not one of the supported
            packing types or if the number of circles is not a positive
            integer.
    """
    # Check if a valid packing type is provided
    if not _is_valid_packing_type(packing_type):
        raise ValueError(f"Invalid packing type: '{packing_type}' is not supported.")

    # Check if the number of circles is a positive integer
    if not isinstance(num_circles, int) or num_circles < 1:
        raise ValueError("Number of circles must be a positive integer.")

    packing_type = packing_type.lower()
    radius_function, monotonicity = constants.PACKING_TYPES_DICT[packing_type]
    function_values = np.array([radius_function(n + 1) for n in range(num_circles)])

    # If the function "radius_function" is decreasing, we reverse the order of
    # "function_values" so that the values are listed in increasing order
    if monotonicity == "decreasing":
        function_values.sort()

    ratio = largest_radius / function_values[-1]
    radii = function_values * ratio

    return radii


def _convert_coordinates_to_pixels(
        rel_coordinates: np.ndarray,
        image_size: int
) -> np.ndarray:
    """Convert relative coordinates to pixel values based on the size of
       a square image.

    The function takes relative coordinates in the range of [-1, 1] and
    converts them to pixel values based on the size of a square image.
    The relative coordinates are assumed to be in normalized form, where
    the origin (0, 0) corresponds to the center of the image and the
    values (-1, -1) and (1, 1) correspond to the lower left and upper
    right corner of the image, respectively.

    Args:
        rel_coordinates (np.ndarray): Relative coordinates in the range
            of [-1, 1].
        image_size (int): Size of the square image that coordinates are
            to be based on.

    Returns:
        np.ndarray: Pixel values corresponding to the relative
            coordinates.

    Raises:
        ValueError: If the relative coordinates are outside the range of
            [-1, 1] or if the image size is not a positive integer.
    """
    # Check if the relative coordinates are within the range of [-1, 1]
    if np.any((rel_coordinates < -1) | (rel_coordinates > 1)):
        raise ValueError("Relative coordinates must be in the range of [-1, 1].")

    # Check if the image size is a positive integer
    if not isinstance(image_size, int) or image_size < 1:
        raise ValueError("Image size must be a positive integer.")

    # Shift coordinates from [-1, 1] to [0, 1]
    rel_coordinates = rel_coordinates / 2 + 0.5

    # Scale coordinates from [0, 1] to [0, card_size] and convert to integer values
    coordinates = np.floor(rel_coordinates * image_size).astype("int")

    return coordinates


def _convert_radii_to_pixels(
        rel_radii: np.ndarray,
        image_size: int
) -> np.ndarray:
    """Convert relative radii to pixel values based on the size of a
       square image.

    Args:
        rel_radii (np.ndarray): Relative radii in the range of [0, 1].
        image_size (int): Size of the square image that radii are to be
            based on.

    Returns:
        np.ndarray: Pixel values corresponding to the relative radii.

    Raises:
        ValueError: If the relative radius is outside the valid range of
            [0, 1] or if the image size is not a positive integer.
    """
    # Check if the relative radii are within the range of [0, 1]
    if np.any((rel_radii < -1) | (rel_radii > 1)):
        raise ValueError("Relative radii must be in the range of [0, 1].")

    # Check if the image size is a positive integer
    if not isinstance(image_size, int) or image_size < 1:
        raise ValueError("Image size must be a positive integer.")

    radii = np.floor(rel_radii * image_size).astype("int")

    return radii


def get_packing_data(
        num_circles: int,
        packing_type: str,
        image_size: int
) -> dict[str, np.ndarray]:
    """Get data (coordinates and radii) of a specified packing in pixel
       values.

    Args:
        num_circles (int): Total number of circles in the packing.
        packing_type (str): Type of circle packing.
        image_size (int): Size of the square image that coordinates and
            radii are to be based on.

    Returns:
        dict[str, np.ndarray]: A dictionary containing the coordinates
            and radii in pixel values.
    """
    # Get coordinates
    coordinates = _convert_coordinates_to_pixels(
        _read_coordinates_from_file(num_circles, packing_type), image_size
    )

    # Get radii (i.e., sizes of the circles in pixels)
    largest_radius = _read_radius_from_file(num_circles, packing_type)
    radii = _convert_radii_to_pixels(
        _compute_radii(num_circles, packing_type, largest_radius), image_size
    )

    # Combine into dictionary
    packing_data = {
        "coordinates": coordinates,
        "radii": radii
    }

    return packing_data
