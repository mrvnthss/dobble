# pylint: disable=missing-function-docstring, missing-module-docstring

from dobble import utils


INTEGER = 41
INTEGER_AS_FLOAT = 41.0
NON_INTEGER = 41.5

NEGATIVE_NUMBER = -7

NON_PRIME_NUMBER = 2 * 7
LARGE_NON_PRIME_NUMBER = 10 * 792

PRIME_NUMBER = 241
LARGE_PRIME_NUMBER = 7919

NON_PRIME_POWER = 2 * 5
LARGE_NON_PRIME_POWER = (2 * 5) ** 4

PRIME_POWER = 2 ** 3
LARGE_PRIME_POWER = 3 ** 5


def test_is_integer_with_integer():
    assert utils.is_integer(INTEGER)


def test_is_integer_with_integer_as_float():
    assert utils.is_integer(INTEGER_AS_FLOAT)


def test_is_integer_with_non_integer():
    assert not utils.is_integer(NON_INTEGER)


def test_is_prime_with_zero():
    assert not utils.is_prime(0)


def test_is_prime_with_one():
    assert not utils.is_prime(1)


def test_is_prime_with_negative_number():
    assert not utils.is_prime(NEGATIVE_NUMBER)


def test_is_prime_with_non_prime_number():
    assert not utils.is_prime(NON_PRIME_NUMBER)


def test_is_prime_with_large_non_prime_number():
    assert not utils.is_prime(LARGE_NON_PRIME_NUMBER)


def test_is_prime_with_prime_number():
    assert utils.is_prime(PRIME_NUMBER)


def test_is_prime_with_large_prime_number():
    assert utils.is_prime(LARGE_PRIME_NUMBER)


def test_is_prime_power_with_zero():
    assert not utils.is_prime_power(0)


def test_is_prime_power_with_one():
    assert not utils.is_prime_power(1)


def test_is_prime_power_with_negative_number():
    assert not utils.is_prime_power(NEGATIVE_NUMBER)


def test_is_prime_power_with_non_prime_power():
    assert not utils.is_prime_power(NON_PRIME_POWER)


def test_is_prime_power_with_large_non_prime_power():
    assert not utils.is_prime_power(LARGE_NON_PRIME_POWER)


def test_is_prime_power_with_prime_power():
    assert utils.is_prime_power(PRIME_POWER)


def test_is_prime_power_with_large_prime_power():
    assert utils.is_prime_power(LARGE_PRIME_POWER)
