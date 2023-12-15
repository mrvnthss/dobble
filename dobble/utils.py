"""Utility functions for finite projective planes.

This module provides functions for computing incidence matrices for finite projective planes.

Functions:
    - _is_prime: Check if a number is prime.
    - _is_prime_power: Check if a number is a prime power.
    - compute_incidence_matrix: Compute the incidence matrix of a finite projective plane.
"""

# Standard Library Imports
import math

# Third-Party Library Imports
import numpy as np


def _is_prime(num: float) -> bool:
    """Check if a number is prime.

    Args:
        num (float): The number to be checked.

    Returns:
        bool: True if the number is prime, False otherwise.
    """
    is_integer = isinstance(num, int) or (isinstance(num, float) and num.is_integer())

    if not is_integer or num <= 1:
        return False

    # Check for non-trivial factors
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def _is_prime_power(num: float) -> bool:
    """Check if a number is a prime power.

    Args:
        num (float): The number to be checked.

    Returns:
        bool: True if the number is a prime power, False otherwise.
    """
    is_integer = isinstance(num, int) or (isinstance(num, float) and num.is_integer())

    if not is_integer or num <= 1:
        return False

    # Compute the i-th root of num and check if it's prime
    for i in range(1, int(math.log2(num)) + 1):
        root = num ** (1 / i)
        if root.is_integer() and _is_prime(root):
            return True
    return False


def compute_incidence_matrix(order: int) -> np.ndarray:
    """Compute the incidence matrix of a finite projective plane with specified order.

    Args:
        order (int): The order of the finite projective plane.

    Returns:
        np.ndarray: The computed incidence matrix.  Rows correspond to lines and columns correspond to points.

    Raises:
        ValueError: If the argument order is not a prime power.

    Example:
        >>> compute_incidence_matrix(2)
        array([[ True,  True,  True, False, False, False, False],
               [ True, False, False,  True,  True, False, False],
               [ True, False, False, False, False,  True,  True],
               [False,  True, False,  True, False,  True, False],
               [False,  True, False, False,  True, False,  True],
               [False, False,  True,  True, False, False,  True],
               [False, False,  True, False,  True,  True, False]])
    """
    if not _is_prime_power(order):
        raise ValueError("The argument 'order' must be a prime power.")

    # Number of points/lines of a finite projective plane of order n is given by n^2 + n + 1
    size = order ** 2 + order + 1

    # Preallocate incidence matrix, where rows correspond to lines and columns correspond to points
    incidence_matrix = np.zeros((size, size), dtype=bool)

    # Determine which points are on the first line
    which_line = 0
    which_pts = list(range(order + 1))
    incidence_matrix[which_line, which_pts] = True

    # Determine which points are on the next n lines
    for line in range(order):
        which_line += 1
        # The first n + 1 lines will all share point '0'
        which_pts = [0]
        start = (line + 1) * order + 1
        end = start + order
        which_pts.extend(list(range(start, end)))
        incidence_matrix[which_line, which_pts] = True

    # Determine which points are on the final n^2 lines
    for block in range(order):
        for line in range(order):
            which_line += 1
            which_pts = [block + 1]
            for pt in range(order):
                which_pts.append(order * (pt + 1) + ((block * pt + line) % order) + 1)
            incidence_matrix[which_line, which_pts] = True

    return incidence_matrix
