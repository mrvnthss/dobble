"""Functions to compute incidence matrices of FPPs.

Functions:
    * _get_permutation_matrix: Return the permutation matrix
        corresponding to a permutation.
    * compute_incidence_matrix: Compute the canonical incidence matrix
        of a finite projective plane.
"""


import numpy as np

from . import constants
from . import utils


def _get_permutation_matrix(permutation: np.ndarray) -> np.ndarray:
    """Return the permutation matrix corresponding to a permutation.

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
    points.  "1" entries indicate that a given line and point are
    incident, while "0" entries indicate the opposite.

    Args:
        order: The order of the finite projective plane.  Must be prime
          or one of the prime powers 4 and 8.

    Returns:
        The computed incidence matrix.

    Raises:
        ValueError: If the argument order is neither a prime number nor
          one of the prime powers 4 and 8.

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

    is_prime = utils.is_prime(order)

    if not (is_prime or order in list(constants.FPP_KERNELS)):
        raise ValueError(
            "The argument 'order' must be a prime number or one of: "
            + ", ".join(map(str, list(constants.FPP_KERNELS)))
        )

    # Set up incidence matrix, where rows correspond to lines, and columns correspond to points
    incidence_matrix = np.zeros(
        (order ** 2 + order + 1, order ** 2 + order + 1),
        dtype=np.uint8
    )

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
            if is_prime:
                leading_entry = (1 + i * j) % order
                if leading_entry == 0:
                    leading_entry = order
                permutation = (np.array(range(0, order)) + leading_entry) % order
                permutation[permutation == 0] = order
            else:
                permutation = constants.FPP_KERNELS[order][i - 1, j - 1, :]
            permutation_matrix = _get_permutation_matrix(permutation)

        # Place permutation matrix C_{ij} in incidence matrix
        start_row = order + 1 + i * order
        start_col = order + 1 + j * order
        end_row = start_row + order
        end_col = start_col + order
        incidence_matrix[start_row:end_row, start_col:end_col] = permutation_matrix

    return incidence_matrix
