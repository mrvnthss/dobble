# pylint: disable=protected-access, missing-function-docstring, missing-module-docstring

import numpy as np
import pytest

from dobble import constants
from dobble import planes


INTEGER = 41
INTEGER_AS_FLOAT = 41.0
NON_INTEGER = 41.5

NEGATIVE_NUMBER = -7

NON_PRIME_NUMBER = 2 * 7
LARGE_NON_PRIME_NUMBER = 10 * 792

SMALL_PRIME_NUMBER = 2
PRIME_NUMBER = 241
LARGE_PRIME_NUMBER = 7919

NON_PRIME_POWER = 2 * 5
LARGE_NON_PRIME_POWER = (2 * 5) ** 4

PRIME_POWER = 2 ** 3
LARGE_PRIME_POWER = 3 ** 5

INVALID_PERMUTATION = np.array([2, 1, 4])
VALID_PERMUTATION = np.array([2, 4, 1, 3])


def is_incidence_matrix_of_fpp(matrix: np.ndarray, order: int) -> bool:
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

    is_incidence_matrix = np.all(matrix @ matrix.T == order * identity + all_ones)

    return is_incidence_matrix


def test_is_integer_with_integer():
    assert planes._is_integer(INTEGER)


def test_is_integer_with_integer_as_float():
    assert planes._is_integer(INTEGER_AS_FLOAT)


def test_is_integer_with_non_integer():
    assert not planes._is_integer(NON_INTEGER)


def test_is_prime_with_zero():
    assert not planes._is_prime(0)


def test_is_prime_with_one():
    assert not planes._is_prime(1)


def test_is_prime_with_negative_number():
    assert not planes._is_prime(NEGATIVE_NUMBER)


def test_is_prime_with_non_prime_number():
    assert not planes._is_prime(NON_PRIME_NUMBER)


def test_is_prime_with_large_non_prime_number():
    assert not planes._is_prime(LARGE_NON_PRIME_NUMBER)


def test_is_prime_with_prime_number():
    assert planes._is_prime(PRIME_NUMBER)


def test_is_prime_with_large_prime_number():
    assert planes._is_prime(LARGE_PRIME_NUMBER)


def test_is_prime_power_with_zero():
    assert not planes._is_prime_power(0)


def test_is_prime_power_with_one():
    assert not planes._is_prime_power(1)


def test_is_prime_power_with_negative_number():
    assert not planes._is_prime_power(NEGATIVE_NUMBER)


def test_is_prime_power_with_non_prime_power():
    assert not planes._is_prime_power(NON_PRIME_POWER)


def test_is_prime_power_with_large_non_prime_power():
    assert not planes._is_prime_power(LARGE_NON_PRIME_POWER)


def test_is_prime_power_with_prime_power():
    assert planes._is_prime_power(PRIME_POWER)


def test_is_prime_power_with_large_prime_power():
    assert planes._is_prime_power(LARGE_PRIME_POWER)


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


def test_compute_incidence_matrix_with_primes_up_to_50():
    for num in range(1, 51):
        if planes._is_prime(num):
            result = planes.compute_incidence_matrix(num)
            assert is_incidence_matrix_of_fpp(result, num)


def test_compute_incidence_matrix_with_implemented_prime_powers():
    for num in constants.PERMUTATIONS:
        result = planes.compute_incidence_matrix(num)
        assert is_incidence_matrix_of_fpp(result, num)