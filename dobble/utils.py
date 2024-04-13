"""Utility functions for finite projective planes.

This module provides functions for computing incidence matrices for
finite projective planes.

Functions:
    - _is_prime: Check if a number is prime.
    - _is_prime_power: Check if a number is a prime power.
    - _get_permutation_matrix: Return the permutation matrix
        corresponding to the permutation.
    - compute_incidence_matrix: Compute the incidence matrix of a finite
        projective plane.
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


def _get_permutation_matrix(permutation: np.ndarray) -> np.ndarray:
    """Return the permutation matrix corresponding to the permutation.

    Args:
        permutation (np.ndarray): The permutation to be converted to a
            permutation matrix.

    Returns:
        np.ndarray: The permutation matrix corresponding to the
            permutation.

    Raises:
        ValueError: If the passed argument is not a valid permutation.
    """
    # Check if the permutation is valid
    if (not isinstance(permutation, np.ndarray)
            or permutation.ndim != 1
            or set(permutation) != set(range(1, len(permutation) + 1))
            or len(permutation) == 0):
        raise ValueError("Invalid permutation.")

    # Construct permutation matrix
    size = len(permutation)
    permutation_matrix = np.zeros((size, size), dtype=np.uint8)
    permutation_matrix[np.arange(size), permutation - 1] = 1

    return permutation_matrix


def compute_incidence_matrix(order: int) -> np.ndarray:
    """Compute the incidence matrix of a finite projective plane with
       specified order.

    Args:
        order (int): The order of the finite projective plane.

    Returns:
        np.ndarray: The computed incidence matrix.  Rows correspond to
            lines and columns correspond to points.

    Raises:
        ValueError: If the argument order is not a prime.

    Example:
        >>> compute_incidence_matrix(2)
        array([[1, 1, 1, 0, 0, 0, 0],
               [1, 0, 0, 1, 1, 0, 0],
               [1, 0, 0, 0, 0, 1, 1],
               [0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 0, 1, 0, 1],
               [0, 0, 1, 1, 0, 0, 1],
               [0, 0, 1, 0, 1, 1, 0]], dtype=uint8)
    """
    if not _is_prime(order):
        raise ValueError("The argument 'order' must be a prime.")

    # Number of points/lines of a finite projective plane of order n is given by n^2 + n + 1
    size = order ** 2 + order + 1

    # Preallocate incidence matrix
    #   - rows correspond to lines
    #   - columns correspond to points
    incidence_matrix = np.zeros((size, size), dtype=np.uint8)

    # Place 1s in upper left block
    incidence_matrix[0, : order + 1] = 1
    incidence_matrix[: order + 1, 0] = 1

    # Place 1s in remaining boundary blocks (i.e., top row & leftmost column of blocks)
    start = order + 1
    for block in range(1, order + 1):
        stop = start + order
        # top row of blocks
        incidence_matrix[block, start:stop] = 1
        # leftmost column of blocks
        incidence_matrix[start:stop, block] = 1
        start = stop

    # Place 1s in remaining n x n block matrix
    # NOTE: Each block is an n x n permutation matrix
    for row, col in np.ndindex(order, order):
        # Determine permutation matrix
        if row == 0 or col == 0:
            permutation_matrix = np.eye(order, dtype=np.uint8)
        else:
            leading_entry = (1 + row * col) % order
            if leading_entry == 0:
                leading_entry = order
            permutation = (np.array(range(0, order)) + leading_entry) % order
            permutation[permutation == 0] = order
            permutation_matrix = _get_permutation_matrix(permutation)

        # Place permutation matrix in incidence matrix
        start_row = order + 1 + row * order
        start_col = order + 1 + col * order
        end_row = start_row + order
        end_col = start_col + order
        incidence_matrix[start_row:end_row, start_col:end_col] = permutation_matrix

    return incidence_matrix
