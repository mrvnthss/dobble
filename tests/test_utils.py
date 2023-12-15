# Third-Party Library Imports
import numpy as np
import pytest

# Local Imports
from dobble import utils


def test_is_prime_with_zero():
    assert not utils._is_prime(0)


def test_is_prime_with_one():
    assert not utils._is_prime(1)


def test_is_prime_with_negative_number():
    assert not utils._is_prime(-7)


def test_is_prime_with_prime_number():
    assert utils._is_prime(7)


def test_is_prime_with_non_prime_number():
    assert not utils._is_prime(8)


def test_is_prime_with_large_prime_number():
    assert utils._is_prime(7919)


def test_is_prime_with_large_non_prime_number():
    assert not utils._is_prime(7920)


def test_is_prime_power_with_zero():
    assert not utils._is_prime_power(0)


def test_is_prime_power_with_one():
    assert not utils._is_prime_power(1)


def test_is_prime_power_with_negative_number():
    assert not utils._is_prime_power(-8)


def test_is_prime_power_with_prime_power():
    assert utils._is_prime_power(8)


def test_is_prime_power_with_non_prime_power():
    assert not utils._is_prime_power(10)


def test_is_prime_power_with_large_prime_power():
    assert utils._is_prime_power(6561)  # 6561 = 3^8


def test_is_prime_power_with_large_non_prime_power():
    assert not utils._is_prime_power(10000)  # 10^4


def test_compute_incidence_matrix_with_zero():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(0)


def test_compute_incidence_matrix_with_one():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(1)


def test_compute_incidence_matrix_with_negative_number():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(-2)


def test_compute_incidence_matrix_with_prime_power():
    expected_matrix = np.array([
        [True, True, True, False, False, False, False],
        [True, False, False, True, True, False, False],
        [True, False, False, False, False, True, True],
        [False, True, False, True, False, True, False],
        [False, True, False, False, True, False, True],
        [False, False, True, True, False, False, True],
        [False, False, True, False, True, True, False]
    ])
    np.testing.assert_array_equal(utils.compute_incidence_matrix(2), expected_matrix)


def test_compute_incidence_matrix_with_large_prime_power():
    # This test is more of a performance test, as we don't check the result
    utils.compute_incidence_matrix(81)  # 81 = 3^4


def test_compute_incidence_matrix_with_non_prime_power():
    with pytest.raises(ValueError):
        utils.compute_incidence_matrix(6)  # 6 = 2 * 3
