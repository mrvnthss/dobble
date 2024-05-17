"""This module provides utility functions for finite projective planes.

Functions:
    _is_integer: Check if a number is an integer.
    _is_prime: Check if a number is prime.
    _is_prime_power: Check if a number is a prime power.
    _get_permutation_matrix: Return the permutation matrix corresponding
      to the permutation.
    compute_incidence_matrix: Compute the canonical incidence matrix of
      a finite projective plane.
"""


import math

import numpy as np


def _is_integer(num: int | float) -> bool:
    """Check if a number is an integer.

    Args:
        num: The number to be checked.

    Returns:
        True if num is an integer, False otherwise.
    """
    return isinstance(num, int) or (isinstance(num, float) and num.is_integer())


def _is_prime(num: int | float) -> bool:
    """Check if a number is prime.

    Args:
        num: The number to be checked.

    Returns:
        True if num is a prime number, False otherwise.
    """
    is_prime = True

    if not _is_integer(num) or num <= 1:
        is_prime = False
    else:
        # Check for non-trivial factors
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
    return is_prime


def _is_prime_power(num: int | float) -> bool:
    """Check if a number is a prime power.

    Args:
        num: The number to be checked.

    Returns:
        True if num is a prime power, False otherwise.
    """
    is_prime_power = False

    if _is_integer(num) and num > 1:
        # Compute the i-th root of num and check if it's prime
        for i in range(1, int(math.log2(num)) + 1):
            root = num ** (1 / i)
            if _is_integer(root) and _is_prime(root):
                is_prime_power = True
                break
    return is_prime_power


def _get_permutation_matrix(permutation: np.ndarray) -> np.ndarray:
    """Return the permutation matrix corresponding to the permutation.

    Args:
        permutation: The permutation to be converted to a permutation
          matrix.

    Returns:
        The permutation matrix corresponding to the permutation.

    Raises:
        ValueError: If the argument is not a valid permutation.
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
    """Compute the canonical incidence matrix of an FPP.

    This function computes the canonical incidence matrix of a finite
    projective plane (FPP) of prime order based on the construction by
    Paige and Wexler (1953).  The incidence matrix is a square matrix
    with rows corresponding to lines and columns corresponding to
    points.

    Args:
        order: The order of the finite projective plane.

    Returns:
        The computed incidence matrix.

    Raises:
        ValueError: If the argument order is not a prime number.

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

    # Number of points/lines of an FPP of order n
    size = order ** 2 + order + 1

    # Set up incidence matrix, where rows correspond to lines, and columns correspond to points
    incidence_matrix = np.zeros((size, size), dtype=np.uint8)

    # a) P_1, P_2, ..., P_{n+1} are the points of L_1
    incidence_matrix[0, : order + 1] = 1

    # b) L_1, L_2, ..., L_{n+1} are the lines through P_1
    incidence_matrix[: order + 1, 0] = 1

    start = order + 1
    for block in range(1, order + 1):
        stop = start + order

        # c) P_{kn+2}, P_{kn+3}, ..., P_{kn+n+1} lie on L_{k+1}, k = 1, 2, ..., n
        incidence_matrix[block, start:stop] = 1

        # d) L_{kn+2}, L_{kn+3}, ..., L_{kn+n+1} lie on P_{k+1}, k = 1, 2, ..., n
        incidence_matrix[start:stop, block] = 1
        start = stop

    # Kernel of the incidence matrix (i.e., n^2 permutation matrices C_{ij})
    for i, j in np.ndindex(order, order):
        # Determine permutation matrix C_{ij}
        if i == 0 or j == 0:
            permutation_matrix = np.eye(order, dtype=np.uint8)
        else:
            leading_entry = (1 + i * j) % order
            if leading_entry == 0:
                leading_entry = order
            permutation = (np.array(range(0, order)) + leading_entry) % order
            permutation[permutation == 0] = order
            permutation_matrix = _get_permutation_matrix(permutation)

        # Place permutation matrix C_{ij} in incidence matrix
        start_row = order + 1 + i * order
        start_col = order + 1 + j * order
        end_row = start_row + order
        end_col = start_col + order
        incidence_matrix[start_row:end_row, start_col:end_col] = permutation_matrix

    return incidence_matrix
