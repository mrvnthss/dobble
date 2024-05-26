# pylint: disable=missing-function-docstring, missing-module-docstring

from importlib.resources import files

import numpy as np
from PIL import Image
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


def test_emoji_init_with_valid_emoji_name():
    emoji = Emoji(VALID_EMOJI_NAME)
    assert emoji.name == VALID_EMOJI_NAME
    assert emoji.rotation == 0


def test_emoji_init_with_classic_dobble_emojis():
    for name in constants.CLASSIC_DOBBLE_EMOJIS:
        emoji = Emoji(name)
        assert emoji.name == name
        assert emoji.rotation == 0


def test_emoji_init_with_invalid_emoji_name():
    with pytest.raises(ValueError):
        Emoji(INVALID_EMOJI_NAME)


def test_emoji_rotate():
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(30)
    assert emoji.rotation == 30
    emoji.rotate(-45)
    assert emoji.rotation == 345
    emoji.rotate(15)
    assert emoji.rotation == 0


def test_emoji_show(mocker):
    mock_show = mocker.patch("PIL.Image.Image.show")
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.show()
    mock_show.assert_called_once()


def test_emoji_get_img_with_color_img():
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_img = emoji.get_img(outline_only=False, padding=0.1)
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
        padding=0.1
    )
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_img_with_bw_img():
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_img = emoji.get_img(outline_only=True, padding=0.1)
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
        padding=0.1
    )
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_img_with_color_img_and_rotation():
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(45)
    returned_img = emoji.get_img(outline_only=False, padding=0.05)
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
        padding=0.05
    ).rotate(45)
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_img_with_bw_img_and_rotation():
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(-30)
    returned_img = emoji.get_img(outline_only=True, padding=0.05)
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
        padding=0.05
    ).rotate(-30)
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_emoji_get_array_with_color_img():
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_array = emoji.get_array(outline_only=False, padding=0.1)
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
            padding=0.1
        )
    )
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_array_with_bw_img():
    emoji = Emoji(VALID_EMOJI_NAME)
    returned_array = emoji.get_array(outline_only=True, padding=0.1)
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
            padding=0.1
        )
    )
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_array_with_color_img_and_rotation():
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(60)
    returned_array = emoji.get_array(outline_only=False, padding=0.2)
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
            padding=0.2
        ).rotate(60)
    )
    np.testing.assert_array_equal(returned_array, expected_array)


def test_emoji_get_array_with_bw_img_and_rotation():
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.rotate(-90)
    returned_array = emoji.get_array(outline_only=True, padding=0.2)
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
            padding=0.2
        ).rotate(-90)
    )
    np.testing.assert_array_equal(returned_array, expected_array)
