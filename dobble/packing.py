"""Utility functions for handling circle packing data.

This module provides functions to read circle packing data from files, and convert relative coordinates to pixel values
for rendering on images.

Functions:
    - _read_coordinates_from_file: Read coordinates of circles from a text file.
    - _read_radius_from_file: Read the radius of the largest circle in each packing from a text file.
    - _compute_radii: Compute the radii of all circles in a packing.
    - _convert_coordinates_to_pixels: Convert relative coordinates to pixel values.
    - _convert_radius_to_pixels: Convert a relative radius to a pixel value.
    - get_packing_data: Get packing data (coordinates and sizes) and convert to pixel values.

The module uses the 'constants' module from the 'dobble' package to access the project-level constants, and in
particular, the paths to the packing data files.
"""

# Standard Library Imports
from importlib import resources

# Third-Party Library Imports
import numpy as np

# Local Imports
from . import constants


def _read_coordinates_from_file(num_circles: int, packing_type: str) -> list[list[float]]:
    """Read the coordinates of the specified circle packing from a text file.

    Args:
        num_circles (int): Number of circles in the packing.
        packing_type (str): Type of circle packing.

    Returns:
        list[list[float]]: The coordinates of the circles in the packing.

    Raises:
        FileNotFoundError: If the text file for the specified packing type and number of circles is not found.
    """
    file_name = packing_type + str(num_circles) + '.txt'

    try:
        with resources.open_text(f'{constants.PACKING_DIR}.{packing_type}', file_name) as file:
            # Read values line by line, split into separate columns and get rid of first column of text file
            coordinates = [line.strip().split()[1:] for line in file.readlines()]
            coordinates = [[float(coordinate) for coordinate in coordinates_list] for coordinates_list in coordinates]
        return coordinates
    except FileNotFoundError:
        raise FileNotFoundError(f"Coordinates file for '{packing_type}' packing with {num_circles} circles not found.")


def _read_radius_from_file(num_circles: int, packing_type: str) -> float:
    """Read the radius of the largest circle of the specified circle packing from a text file.

    Args:
        num_circles (int): Number of circles in the packing.
        packing_type (str): Type of circle packing.

    Returns:
        float: The radius of the largest circle of the packing.

    Raises:
        FileNotFoundError: If the text file for the specified packing type is not found.
        ValueError: If no radius is found for the specified packing type and number of circles.
    """
    file_name = constants.RADIUS_TXT

    try:
        with resources.open_text(f'{constants.PACKING_DIR}.{packing_type}', file_name) as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 2 and int(values[0]) == num_circles:
                    return float(values[1])
        raise ValueError(f"No radius found for packing type '{packing_type}' with {num_circles} circles.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Radius file for '{packing_type}' packing not found.")


def _compute_radii(num_circles: int, packing_type: str, largest_radius: float) -> list[float]:
    """Compute the radii of circles in a circle packing.

    Args:
        num_circles (int): Total number of circles in the packing.
        packing_type (str): Type of circle packing.
        largest_radius (float): Radius of the largest circle in the packing.

    Returns:
        list[float]: The computed radii of the circles in the packing.
    """
    radius_function, monotonicity = constants.PACKING_TYPES_DICT[packing_type]
    function_values = [radius_function(n + 1) for n in range(num_circles)]

    # If the function 'radius_function' is decreasing, we reverse the order of 'function_values' so that the values are
    # listed in increasing order
    function_values.reverse() if monotonicity == 'decreasing' else None

    ratio = largest_radius / function_values[-1]
    radii = [function_values[n] * ratio for n in range(num_circles)]

    return radii


def _convert_coordinates_to_pixels(
        rel_coordinates: np.ndarray[float, float] | tuple[float, float], image_size: int) -> tuple[int, int]:
    """Convert relative coordinates to pixel values based on the size of a square image.

    The function takes relative coordinates in the range of [-1, 1] and converts them to pixel values
    based on the size of a square image.  The relative coordinates are assumed to be in normalized form,
    where the origin (0, 0) corresponds to the center of the image and the values (-1, -1) and (1, 1)
    correspond to the lower left and upper right corner of the image, respectively.

    Args:
        rel_coordinates (np.ndarray[float, float] | tuple[float, float]): Relative coordinates in the range of [-1, 1].
        image_size (int): Size of the square image that coordinates are to be based on.

    Returns:
        tuple[int, int]: Pixel values corresponding to the relative coordinates.

    Raises:
        ValueError: If the relative coordinates are outside the range of [-1, 1].
    """
    # Convert rel_coordinates to NumPy array if necessary
    rel_coordinates = np.array(rel_coordinates) if not isinstance(rel_coordinates, np.ndarray) else rel_coordinates

    # Check if the relative coordinates are within the range of [-1, 1]
    if np.any((rel_coordinates < -1) | (rel_coordinates > 1)):
        raise ValueError('Relative coordinates must be in the range of [-1, 1].')

    # Shift coordinates from [-1, 1] to [0, 1]
    rel_coordinates = rel_coordinates / 2 + 0.5

    # Scale coordinates from [0, 1] to [0, card_size] and convert to integer values
    coordinates = np.floor(rel_coordinates * image_size).astype('int')

    return tuple(coordinates)


def _convert_radius_to_pixels(rel_radius: float, image_size: int) -> int:
    """Convert relative radius to pixel value based on the size of a square image.

    Args:
        rel_radius (float): Relative radius in the range of [0, 1].
        image_size (int): Size of the square image that radii are to be based on.

    Returns:
        int: Pixel value corresponding to the relative radius.

    Raises:
        ValueError: If the relative radius is outside the valid range of [0, 1].
    """
    if rel_radius < 0 or rel_radius > 1:
        raise ValueError('Relative radius must be in the range of [0, 1].')

    size = int(rel_radius * image_size)

    return size


def get_packing_data(num_circles: int, packing_type: str, image_size: int) -> dict[str, list]:
    """
    Args:
        num_circles (int): Total number of circles in the packing.
        packing_type (str): Type of circle packing.
        image_size (int): Size of the square image that coordinates and radii are to be based on.

    Returns:
        dict[str, list]: A dictionary containing the coordinates and sizes in pixel values.

    Raises:
        ValueError: If the packing type is not one of the supported packing types.
    """
    if packing_type not in constants.PACKING_TYPES_DICT:
        raise ValueError(f"Invalid packing type: '{packing_type}' is not supported.")

    # Coordinates
    rel_coordinates_array = _read_coordinates_from_file(num_circles, packing_type)
    coordinates = [
        _convert_coordinates_to_pixels(rel_coordinates, image_size) for rel_coordinates in rel_coordinates_array
    ]

    # Sizes
    largest_radius = _read_radius_from_file(num_circles, packing_type)
    rel_radii = _compute_radii(num_circles, packing_type, largest_radius)
    sizes = [_convert_radius_to_pixels(rel_radius, image_size) for rel_radius in rel_radii]

    # Combine into dictionary
    packing_data = {
        'coordinates': coordinates,
        'sizes': sizes
    }

    return packing_data
