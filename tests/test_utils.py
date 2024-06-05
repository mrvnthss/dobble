# pylint: disable=missing-function-docstring, missing-module-docstring, protected-access

import numpy as np
import pytest
from PIL import Image, ImageDraw

from dobble import constants
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

INVALID_PERMUTATIONS = [
    [1, 1, 3, 4, 5],
    [1, 2, 2, 3, 4],
    [4, 1, 2],
    [0, 1, 2, 3, 4]
]
VALID_PERMUTATION = [5, 2, 3, 4, 1]

RGB_IMAGE = Image.new("RGB", (100, 100))
NON_SQUARE_IMAGE = Image.new("RGBA", (100, 200))
FULLY_TRANSPARENT_IMAGE = Image.new("RGBA", (100, 100))

NEGATIVE_PADDING = -0.1
INVALID_PADDING = 1

INVALID_EMOJI_NAME = "invalid emoji name"
TEST_EMOJIS = [
    ("sunset", "1F307", "travel-places", "place-other"),
    ("face with tears of joy", "1F602", "smileys-emotion", "face-smiling"),
    ("basketball", "1F3C0", "activities", "sport"),
    ("electric coffee percolator", "E154", "extras-openmoji", "objects")
]

VALID_GROUPS = [
    "activities",
    "animals-nature",
    "component",
    "extras-openmoji",
    "extras-unicode",
    "flags",
    "food-drink",
    "objects",
    "people-body",
    "smileys-emotion",
    "symbols",
    "travel-places"
]
VALID_SUBGROUPS = [
    "alphanum",
    "animal-amphibian",
    "animal-bird",
    "animal-bug",
    "animal-mammal",
    "animal-marine",
    "animal-reptile",
    "animals-nature",
    "arrow",
    "arts-crafts",
    "av-symbol",
    "award-medal",
    "body-parts",
    "book-paper",
    "brand",
    "cat-face",
    "climate-environment",
    "clothing",
    "computer",
    "country-flag",
    "currency",
    "dishware",
    "drink",
    "emergency",
    "emotion",
    "event",
    "face-affection",
    "face-concerned",
    "face-costume",
    "face-glasses",
    "face-hand",
    "face-hat",
    "face-negative",
    "face-neutral-skeptical",
    "face-sleepy",
    "face-smiling",
    "face-tongue",
    "face-unwell",
    "family",
    "flag",
    "flags",
    "food-asian",
    "food-drink",
    "food-fruit",
    "food-marine",
    "food-prepared",
    "food-sweet",
    "food-vegetable",
    "game",
    "gardening",
    "gender",
    "geometric",
    "hair-style",
    "hand-fingers-closed",
    "hand-fingers-open",
    "hand-fingers-partial",
    "hand-prop",
    "hand-single-finger",
    "hands",
    "healthcare",
    "heart",
    "hotel",
    "household",
    "interaction",
    "keycap",
    "light-video",
    "lock",
    "mail",
    "math",
    "medical",
    "money",
    "monkey-face",
    "music",
    "musical-instrument",
    "objects",
    "office",
    "other-object",
    "other-symbol",
    "people",
    "person",
    "person-activity",
    "person-fantasy",
    "person-gesture",
    "person-resting",
    "person-role",
    "person-sport",
    "person-symbol",
    "phone",
    "place-building",
    "place-geographic",
    "place-map",
    "place-other",
    "place-religious",
    "plant-flower",
    "plant-other",
    "punctuation",
    "regional-indicator",
    "religion",
    "science",
    "skin-tone",
    "sky-weather",
    "smileys-emotion",
    "sound",
    "sport",
    "subdivision-flag",
    "symbol-other",
    "symbols",
    "technology",
    "time",
    "tool",
    "transport-air",
    "transport-ground",
    "transport-sign",
    "transport-water",
    "travel-places",
    "ui-element",
    "warning",
    "writing",
    "zodiac"
]
INVALID_GROUP = "food"
INVALID_SUBGROUP = "exercise"

INVALID_PACKING = "ccid"
VALID_NUM_CIRCLES = list(range(5, 51))
INVALID_LAYOUTS = [
    ("cci", 51),
    ("ccib", 1),
    ("ccic", 2),
    ("ccir", 3),
    ("ccis", 4)
]
VALID_LAYOUTS = [
    (packing, num_circles) for packing, data in constants.PACKINGS_DICT.items()
    for num_circles in data[1]
]


def test_get_emoji_group_with_invalid_emoji_name():
    with pytest.raises(ValueError):
        utils.get_emoji_group(INVALID_EMOJI_NAME)


@pytest.mark.parametrize("name, _, group, __", TEST_EMOJIS)
def test_get_emoji_group_with_test_emojis(name, group, _, __):
    assert utils.get_emoji_group(name) == group


def test_get_emoji_hexcode_with_invalid_emoji_name():
    with pytest.raises(ValueError):
        utils.get_emoji_hexcode(INVALID_EMOJI_NAME)


@pytest.mark.parametrize("name, hexcode, _, __", TEST_EMOJIS)
def test_get_emoji_hexcode_with_test_emojis(name, hexcode, _, __):
    assert utils.get_emoji_hexcode(name) == hexcode


def test_get_emoji_names_by_group_with_invalid_group_name():
    with pytest.raises(ValueError):
        utils.get_emoji_names_by_group(INVALID_GROUP)


@pytest.mark.parametrize("valid_group_name", VALID_GROUPS)
def test_get_emoji_names_by_group_with_valid_group_name(valid_group_name):
    emoji_names = utils.get_emoji_names_by_group(valid_group_name)
    assert isinstance(emoji_names, list)
    assert all(utils.is_valid_emoji_name(emoji_name) for emoji_name in emoji_names)
    assert all(
        utils._META_DATA[emoji_name]["group"] == valid_group_name for emoji_name in emoji_names
    )


def test_get_emoji_subgroup_with_invalid_emoji_name():
    with pytest.raises(ValueError):
        utils.get_emoji_subgroup(INVALID_EMOJI_NAME)


@pytest.mark.parametrize("name, _, __, subgroup", TEST_EMOJIS)
def test_get_emoji_subgroup_with_test_emojis(name, subgroup, _, __):
    assert utils.get_emoji_subgroup(name) == subgroup


def test_is_integer_with_integer():
    assert utils.is_integer(INTEGER)


def test_is_integer_with_integer_as_float():
    assert utils.is_integer(INTEGER_AS_FLOAT)


def test_is_integer_with_non_integer():
    assert not utils.is_integer(NON_INTEGER)


@pytest.mark.parametrize("packing", constants.PACKINGS_DICT)
def test_is_layout_available_with_negative_num_circles(packing):
    assert not utils.is_layout_available(packing, NEGATIVE_NUMBER)


@pytest.mark.parametrize("packing", constants.PACKINGS_DICT)
def test_is_layout_available_with_zero_num_circles(packing):
    assert not utils.is_layout_available(packing, 0)


@pytest.mark.parametrize("num_circles", VALID_NUM_CIRCLES)
def test_is_layout_available_with_invalid_packing(num_circles):
    assert not utils.is_layout_available(INVALID_PACKING, num_circles)


@pytest.mark.parametrize("packing, num_circles", INVALID_LAYOUTS)
def test_is_layout_available_with_invalid_layouts(packing, num_circles):
    assert not utils.is_layout_available(packing, num_circles)


@pytest.mark.parametrize("packing, num_circles", VALID_LAYOUTS)
def test_is_layout_available_with_valid_layouts(packing, num_circles):
    assert utils.is_layout_available(packing, num_circles)


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


@pytest.mark.parametrize("emoji_name", constants.CLASSIC_DOBBLE_EMOJIS)
def test_is_valid_emoji_name_with_classic_dobble_emojis(emoji_name):
    assert utils.is_valid_emoji_name(emoji_name)
    assert utils.is_valid_emoji_name([emoji_name])


def test_is_valid_emoji_name_with_invalid_emoji_name():
    assert not utils.is_valid_emoji_name(INVALID_EMOJI_NAME)
    assert not utils.is_valid_emoji_name([INVALID_EMOJI_NAME])


def test_is_valid_emoji_name_with_empty_list():
    assert not utils.is_valid_emoji_name([])


def test_is_valid_packing_with_invalid_packing():
    assert not utils.is_valid_packing(INVALID_PACKING)


@pytest.mark.parametrize("packing", constants.PACKINGS_DICT)
def test_is_valid_packing_with_valid_packings(packing):
    assert utils.is_valid_packing(packing)


@pytest.mark.parametrize("invalid_permutation", INVALID_PERMUTATIONS)
def test_is_valid_permutation_with_invalid_permutations(invalid_permutation):
    assert not utils.is_valid_permutation(invalid_permutation)
    assert not utils.is_valid_permutation(np.array(invalid_permutation))


def test_is_valid_permutation_with_valid_permutation():
    assert utils.is_valid_permutation(VALID_PERMUTATION)
    assert utils.is_valid_permutation(np.array(VALID_PERMUTATION))


def test_rescale_img_with_rgb_image():
    with pytest.raises(ValueError):
        utils.rescale_img(RGB_IMAGE)


def test_rescale_img_with_non_square_image():
    with pytest.raises(ValueError):
        utils.rescale_img(NON_SQUARE_IMAGE)


def test_rescale_img_with_negative_padding():
    with pytest.raises(ValueError):
        utils.rescale_img(FULLY_TRANSPARENT_IMAGE, padding=NEGATIVE_PADDING)


def test_rescale_img_with_invalid_padding():
    with pytest.raises(ValueError):
        utils.rescale_img(FULLY_TRANSPARENT_IMAGE, padding=INVALID_PADDING)


def test_rescale_img_with_fully_transparent_image():
    np.testing.assert_array_equal(
        np.array(utils.rescale_img(FULLY_TRANSPARENT_IMAGE)),
        np.array(FULLY_TRANSPARENT_IMAGE)
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
