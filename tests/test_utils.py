# pylint: disable=protected-access, missing-function-docstring

"""Unit tests for the utility functions in the 'dobble' package.

The tests cover all the functions from the 'dobble.utils' module. Each function in this module represents a test case,
and uses the pytest framework for setting up the test, executing it, and checking the results.
"""

# Third-Party Library Imports
import numpy as np
import pytest

# Local Imports
from dobble import utils

# Constants for Testing
NEGATIVE_NUMBER = -7
PRIME_NUMBER = 13
NON_PRIME_NUMBER = 14
LARGE_PRIME_NUMBER = 7919
LARGE_NON_PRIME_NUMBER = 7920
PRIME_POWER = 8
NON_PRIME_POWER = 10
LARGE_PRIME_POWER = 3 ** 5
LARGE_NON_PRIME_POWER = 10 ** 4
SMALL_PRIME_POWER = 2


def test_is_prime_with_zero():
    assert not utils._is_prime(0)


def test_is_prime_with_one():
    assert not utils._is_prime(1)


def test_is_prime_with_negative_number():
    assert not utils._is_prime(NEGATIVE_NUMBER)


def test_is_prime_with_prime_number():
    assert utils._is_prime(PRIME_NUMBER)


def test_is_prime_with_non_prime_number():
    assert not utils._is_prime(NON_PRIME_NUMBER)


def test_is_prime_with_large_prime_number():
    assert utils._is_prime(LARGE_PRIME_NUMBER)


def test_is_prime_with_large_non_prime_number():
    assert not utils._is_prime(LARGE_NON_PRIME_NUMBER)


def test_is_prime_power_with_zero():
    assert not utils._is_prime_power(0)


def test_is_prime_power_with_one():
    assert not utils._is_prime_power(1)


def test_is_prime_power_with_negative_number():
    assert not utils._is_prime_power(NEGATIVE_NUMBER)


def test_is_prime_power_with_prime_power():
    assert utils._is_prime_power(PRIME_POWER)


def test_is_prime_power_with_non_prime_power():
    assert not utils._is_prime_power(NON_PRIME_POWER)


def test_is_prime_power_with_large_prime_power():
    assert utils._is_prime_power(LARGE_PRIME_POWER)


def test_is_prime_power_with_large_non_prime_power():
    assert not utils._is_prime_power(LARGE_NON_PRIME_POWER)


def test_compute_incidence_matrix_with_zero():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(0)


def test_compute_incidence_matrix_with_one():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(1)


def test_compute_incidence_matrix_with_negative_number():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(NEGATIVE_NUMBER)


def test_compute_incidence_matrix_with_small_prime_power():
    expected_matrix = np.array([[1, 1, 1, 0, 0, 0, 0],
                                [1, 0, 0, 1, 1, 0, 0],
                                [1, 0, 0, 0, 0, 1, 1],
                                [0, 1, 0, 1, 0, 1, 0],
                                [0, 1, 0, 0, 1, 0, 1],
                                [0, 0, 1, 1, 0, 0, 1],
                                [0, 0, 1, 0, 1, 1, 0]], dtype=np.uint8)

    np.testing.assert_array_equal(utils.compute_incidence_matrix(SMALL_PRIME_POWER), expected_matrix)


def test_compute_incidence_matrix_with_large_prime_power():
    # This test is more of a performance test, as we don't check the result
    utils.compute_incidence_matrix(LARGE_PRIME_POWER)


def test_compute_incidence_matrix_with_non_prime_power():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(NON_PRIME_POWER)
