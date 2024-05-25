# pylint: disable=missing-function-docstring, missing-module-docstring

import numpy as np
from PIL import Image, ImageDraw
import pytest

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

RGB_IMAGE = Image.new("RGB", (100, 100))
NON_SQUARE_IMAGE = Image.new("RGBA", (100, 200))
FULLY_TRANSPARENT_IMAGE = Image.new("RGBA", (100, 100), (0, 0, 0, 0))

NEGATIVE_PADDING = -0.1
INVALID_PADDING = 1


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


def test_rescale_img_with_rgb_image():
    with pytest.raises(ValueError):
        utils.rescale_img(RGB_IMAGE)


def test_rescale_img_with_non_square_image():
    with pytest.raises(ValueError):
        utils.rescale_img(NON_SQUARE_IMAGE)


def test_rescale_img_with_negative_padding():
    with pytest.raises(ValueError):
        utils.rescale_img(RGB_IMAGE, padding=NEGATIVE_PADDING)


def test_rescale_img_with_invalid_padding():
    with pytest.raises(ValueError):
        utils.rescale_img(RGB_IMAGE, padding=INVALID_PADDING)


def test_rescale_img_with_fully_transparent_image():
    np.testing.assert_array_equal(
        np.array(utils.rescale_img(FULLY_TRANSPARENT_IMAGE)), np.array(FULLY_TRANSPARENT_IMAGE)
    )


def test_rescale_img_with_inscribed_circle():
    # Create a transparent square image with white circle of maximum size
    img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, 99, 99], fill="white")

    np.testing.assert_array_equal(
        np.array(utils.rescale_img(img, padding=0)), np.array(img)
    )


def test_rescale_img_with_large_square():
    # Case: target_size < img_size
    # Create a transparent square image with large white square in the center
    img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 90, 90], fill="white")

    # Check that rescaled image contains fewer non-transparent pixels
    rescaled_img = utils.rescale_img(img, padding=0)
    assert np.sum(np.array(rescaled_img)[:, :, -1] > 0) < np.sum(np.array(img)[:, :, -1] > 0)


def test_rescale_img_with_small_square():
    # Case: target_size > img_size
    # Create a transparent square image with small white square in the center
    img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 60, 60], fill="white")

    # Check that rescaled image contains more non-transparent pixels
    rescaled_img = utils.rescale_img(img, padding=0)
    assert np.sum(np.array(rescaled_img)[:, :, -1] > 0) > np.sum(np.array(img)[:, :, -1] > 0)
