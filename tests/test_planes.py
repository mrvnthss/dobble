# pylint: disable=protected-access, missing-function-docstring, missing-module-docstring

import numpy as np
import pytest

from dobble import constants
from dobble import planes
from dobble import utils


NEGATIVE_NUMBER = -7
NON_PRIME_NUMBER = 2 * 7
SMALL_PRIME_NUMBER = 2
PRIMES_UP_TO_50 = [num for num in range(1, 51) if utils.is_prime(num)]

INVALID_PERMUTATION = np.array([2, 1, 4])
VALID_PERMUTATION = np.array([2, 4, 1, 3])


def is_incidence_matrix_of_fpp(
        matrix: np.ndarray,
        order: int
) -> bool:
    """Check if a square matrix is an incidence matrix of an FPP.

    By Theorem 3 of Bruck & Ryser (1949), a square matrix A is an
    incidence matrix of a finite projective plane of order n if it
    satisfies the identity A A^T = n I + J, where I is the identity
    matrix and J is a matrix of all ones.

    Args:
        matrix: The square matrix to be checked.
        order: The order of the finite projective plane.

    Returns:
        True if the matrix is an incidence matrix of a finite projective
          plane, False otherwise.
    """

    size = order ** 2 + order + 1
    all_ones = np.ones((size, size), dtype=np.uint8)
    identity = np.eye(size, dtype=np.uint8)

    return np.all(
        matrix @ matrix.T == order * identity + all_ones
    )


def test_compute_incidence_matrix_with_zero():
    with pytest.raises(ValueError):
        planes.compute_incidence_matrix(0)


def test_compute_incidence_matrix_with_one():
    with pytest.raises(ValueError):
        planes.compute_incidence_matrix(1)


def test_compute_incidence_matrix_with_negative_number():
    with pytest.raises(ValueError):
        planes.compute_incidence_matrix(NEGATIVE_NUMBER)


def test_compute_incidence_matrix_with_non_prime_number():
    with pytest.raises(ValueError):
        planes.compute_incidence_matrix(NON_PRIME_NUMBER)


def test_compute_incidence_matrix_with_small_prime_number():
    expected_matrix = np.array([[1, 1, 1, 0, 0, 0, 0],
                                [1, 0, 0, 1, 1, 0, 0],
                                [1, 0, 0, 0, 0, 1, 1],
                                [0, 1, 0, 1, 0, 1, 0],
                                [0, 1, 0, 0, 1, 0, 1],
                                [0, 0, 1, 1, 0, 0, 1],
                                [0, 0, 1, 0, 1, 1, 0]], dtype=np.uint8)

    result = planes.compute_incidence_matrix(SMALL_PRIME_NUMBER)
    np.testing.assert_array_equal(result, expected_matrix)
    assert is_incidence_matrix_of_fpp(result, SMALL_PRIME_NUMBER)


@pytest.mark.parametrize("order", PRIMES_UP_TO_50)
def test_compute_incidence_matrix_with_primes_up_to_50(order):
    assert is_incidence_matrix_of_fpp(
        planes.compute_incidence_matrix(order),
        order
    )


@pytest.mark.parametrize("order", constants.FPP_KERNELS)
def test_compute_incidence_matrix_with_implemented_prime_powers(order):
    assert is_incidence_matrix_of_fpp(
        planes.compute_incidence_matrix(order),
        order
    )


def test_get_permutation_matrix_with_empty_permutation():
    with pytest.raises(ValueError):
        planes._get_permutation_matrix(np.array([], dtype=np.uint8))


def test_get_permutation_matrix_with_invalid_permutation():
    with pytest.raises(ValueError):
        planes._get_permutation_matrix(INVALID_PERMUTATION)


def test_get_permutation_matrix_with_valid_permutation():
    expected_matrix = np.array([[0, 1, 0, 0],
                                [0, 0, 0, 1],
                                [1, 0, 0, 0],
                                [0, 0, 1, 0]], dtype=np.uint8)
    np.testing.assert_array_equal(
        planes._get_permutation_matrix(VALID_PERMUTATION), expected_matrix
    )
