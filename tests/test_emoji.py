# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name

from importlib.resources import files

import numpy as np
import pytest
from PIL import Image
from PIL.Image import Resampling

from dobble import Emoji
from dobble import constants
from dobble import utils


VALID_EMOJI_NAME = "hand with index finger and thumb crossed: medium-light skin tone"
INVALID_EMOJI_NAME = "invalid emoji name"

VALID_EMOJI_PATH_COLOR = (
        files(constants.OPENMOJI_DIR) / "color" / "people-body" / "1FAF0-1F3FC.png"
)
VALID_EMOJI_PATH_BLACK = (
        files(constants.OPENMOJI_DIR) / "black" / "people-body" / "1FAF0-1F3FC.png"
)


@pytest.fixture
def emoji():
    return Emoji(VALID_EMOJI_NAME)


def test_init_with_invalid_name():
    with pytest.raises(ValueError):
        Emoji(INVALID_EMOJI_NAME)


def test_init_with_valid_name(emoji):
    assert isinstance(emoji, Emoji)
    assert emoji.name == VALID_EMOJI_NAME
    assert emoji.rotation == 0


def test_repr(emoji):
    assert repr(emoji) == (
        "Emoji data\n  Name: hand with index finger and thumb crossed: medium-light skin tone"
        "\n  Hexcode: 1FAF0-1F3FC\n  Group: people-body\n  Subgroup: hand-fingers-partial"
        "\n  Rotation: 0.0 degrees"
    )


def test_get_array_with_default_parameters(emoji):
    returned_array = emoji.get_array()
    expected_array = np.array(
        utils.rescale_img(
            Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
            padding=0
        )
    )
    assert isinstance(returned_array, np.ndarray)
    assert returned_array.shape == (618, 618, 4)
    np.testing.assert_array_equal(returned_array, expected_array)


def test_get_img_with_default_parameters(emoji):
    returned_img = emoji.get_img()
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_COLOR).convert("RGBA"),
        padding=0
    )
    assert isinstance(returned_img, Image.Image)
    assert returned_img.size == (618, 618)
    assert returned_img.mode == "RGBA"
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_get_img_with_non_default_parameters_and_rotation(emoji):
    emoji.rotate(60)
    returned_img = emoji.get_img(
        outline_only=True,
        padding=0.05,
        img_size=128
    )
    expected_img = utils.rescale_img(
        Image.open(VALID_EMOJI_PATH_BLACK).convert("RGBA"),
        padding=0.05
    ).resize(
        (128, 128),
        resample=Resampling.LANCZOS
    ).rotate(
        60,
        resample=Resampling.BICUBIC
    )
    assert isinstance(returned_img, Image.Image)
    assert returned_img.size == (128, 128)
    assert returned_img.mode == "RGBA"
    np.testing.assert_array_equal(
        np.array(returned_img),
        np.array(expected_img)
    )


def test_show(mocker):
    mock_show = mocker.patch("PIL.Image.Image.show")
    emoji = Emoji(VALID_EMOJI_NAME)
    emoji.show()
    mock_show.assert_called_once()
