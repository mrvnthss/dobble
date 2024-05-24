"""Utility functions used in the "dobble" package.

Functions:
    is_integer: Check if a number is an integer.
    is_prime: Check if a number is prime.
    is_prime_power: Check if a number is a prime power.
"""


import math


def is_integer(num: int | float) -> bool:
    """Check if a number is an integer.

    Args:
        num: The number to be checked.

    Returns:
        True if num is an integer, False otherwise.
    """
    return isinstance(num, int) or (isinstance(num, float) and num.is_integer())


def is_prime(num: int | float) -> bool:
    """Check if a number is prime.

    Args:
        num: The number to be checked.

    Returns:
        True if num is a prime number, False otherwise.
    """
    state = True

    if not is_integer(num) or num <= 1:
        state = False
    else:
        # Check for non-trivial factors
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                state = False
                break
    return state


def is_prime_power(num: int | float) -> bool:
    """Check if a number is a prime power.

    Args:
        num: The number to be checked.

    Returns:
        True if num is a prime power, False otherwise.
    """
    state = False

    if is_integer(num) and num > 1:
        # Compute the i-th root of num and check if it's prime
        for i in range(1, int(math.log2(num)) + 1):
            root = num ** (1 / i)
            if is_integer(root) and is_prime(root):
                state = True
                break
    return state
