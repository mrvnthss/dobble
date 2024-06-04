# pylint: disable=missing-function-docstring, missing-module-docstring

from importlib.resources import files

import numpy as np
from PIL import Image
from PIL.Image import Resampling
import pytest

from dobble import constants
from dobble import Emoji
from dobble import utils


VALID_EMOJI_NAME = "hand with index finger and thumb crossed: medium-light skin tone"
INVALID_EMOJI_NAME = "invalid emoji name"

VALID_EMOJI_PATH_COLOR = (
        files(constants.OPENMOJI_DIR) / "color" / "people-body" / "1FAF0-1F3FC.png"
)
VALID_EMOJI_PATH_BLACK = (
        files(constants.OPENMOJI_DIR) / "black" / "people-body" / "1FAF0-1F3FC.png"
)


def test_emoji_init_with_invalid_emoji_name():
    with pytest.raises(ValueError):
        Emoji(INVALID_EMOJI_NAME)


def test_emoji_init_with_valid_emoji_name():
    emoji = Emoji(VALID_EMOJI_NAME)

    # Check that attributes are set correctly
    assert emoji.name == VALID_EMOJI_NAME
    assert emoji.rotation == 0


def test_emoji_init_with_classic_dobble_emojis():
    for name in constants.CLASSIC_DOBBLE_EMOJIS:
        emoji = Emoji(name)
        assert emoji.name == name
        assert emoji.rotation == 0


def test_emoji_get_array_with_bw_img():
    # Create an instance of the Emoji class and call the ``get_array()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_array = emoji.get_array(outline_only=True, padding=0.1)

    # Manually create the expected result
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
            padding=0.1
        )
    )

    # Compare the two arrays
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_array_with_color_img():
    # Create an instance of the Emoji class and call the ``get_array()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_array = emoji.get_array(outline_only=False, padding=0.1)

    # Manually create the expected result
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
            padding=0.1
        )
    )

    # Compare the two arrays
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_array_with_non_default_img_size():
    # Create an instance of the Emoji class and call the ``get_array()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_array = emoji.get_array(outline_only=False, padding=0.05, img_size=256)

    # Manually create the expected result
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
            padding=0.05
        ).resize((256, 256), resample=Resampling.LANCZOS)
    )

    # Compare the two arrays
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_array_with_bw_img_and_rotation():
    # Create an instance of the Emoji class, rotate the emoji, and call the ``get_array()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(-90)
    returned_array = emoji.get_array(outline_only=True, padding=0.2)

    # Manually create the expected result
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
            padding=0.2
        ).rotate(-90, resample=Resampling.BICUBIC)
    )

    # Compare the two arrays
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_array_with_color_img_and_rotation():
    # Create an instance of the Emoji class, rotate the emoji, and call the ``get_array()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(60)
    returned_array = emoji.get_array(outline_only=False, padding=0.2)

    # Manually create the expected result
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
            padding=0.2
        ).rotate(60, resample=Resampling.BICUBIC)
    )

    # Compare the two arrays
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_img_with_bw_img():
    # Create an instance of the Emoji class and call the ``get_img()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_img = emoji.get_img(outline_only=True, padding=0.1)

    # Manually create the expected result
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
        padding=0.1
    )

    # Compare the two images by converting them to NumPy arrays
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_img_with_color_img():
    # Create an instance of the Emoji class and call the ``get_img()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_img = emoji.get_img(outline_only=False, padding=0.1)

    # Manually create the expected result
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
        padding=0.1
    )

    # Compare the two images by converting them to NumPy arrays
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_img_with_non_default_img_size():
    # Create an instance of the Emoji class and call the ``get_img()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_img = emoji.get_img(outline_only=False, padding=0.05, img_size=128)

    # Manually create the expected result
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
        padding=0.05
    ).resize((128, 128), resample=Resampling.LANCZOS)

    # Compare the two images by converting them to NumPy arrays
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_img_with_bw_img_and_rotation():
    # Create an instance of the Emoji class, rotate the emoji, and call the ``get_img()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(-30)
    returned_img = emoji.get_img(outline_only=True, padding=0.05)

    # Manually create the expected result
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
        padding=0.05
    ).rotate(-30, resample=Resampling.BICUBIC)

    # Compare the two images by converting them to NumPy arrays
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_img_with_color_img_and_rotation():
    # Create an instance of the Emoji class, rotate the emoji, and call the ``get_img()`` method
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(45)
    returned_img = emoji.get_img(outline_only=False, padding=0.05)

    # Manually create the expected result
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
        padding=0.05
    ).rotate(45, resample=Resampling.BICUBIC)

    # Compare the two images by converting them to NumPy arrays
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_reset_rotation():
    emoji = Emoji(VALID_EMOJI_NAME)

    # Rotate emoji, then reset rotation, and check that it is back to 0
    emoji.rotate(-70)
    assert emoji.rotation != 0
    emoji.reset_rotation()
    assert emoji.rotation == 0


def test_emoji_rotate():
    emoji = Emoji(VALID_EMOJI_NAME)

    # Rotate card multiple times and check that rotation is as expected
    emoji.rotate(30)
    # (0 + 30) % 360 = 30
    assert emoji.rotation == 30
    emoji.rotate(-45)
    # (30 - 45) % 360 = 345
    assert emoji.rotation == 345
    emoji.rotate(15)
    # (345 + 15) % 360 = 0
    assert emoji.rotation == 0


def test_emoji_show(mocker):
    mock_show = mocker.patch("PIL.Image.Image.show")
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.show()
    mock_show.assert_called_once()
