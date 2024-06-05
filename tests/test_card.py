# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name

import numpy as np
import pytest
from PIL import Image
from PIL.Image import Resampling

from dobble import Card, Emoji
from dobble import constants


INVALID_EMOJI_NAME = "invalid emoji name"
FIVE_VALID_EMOJI_NAMES = [
    "unicorn",
    "dolphin",
    "cheese wedge",
    "bomb",
    "ice"
]
# NOTE: The shuffled list below corresponds to the permutation ``VALID_PERMUTATION``.
FIVE_VALID_EMOJI_NAMES_SHUFFLED = [
    "ice",
    "dolphin",
    "cheese wedge",
    "bomb",
    "unicorn"
]

INVALID_PACKING = "ccid"
INVALID_LAYOUTS = [
    ("ccib", 1),
    ("ccic", 2),
    ("ccir", 3),
    ("ccis", 4)
]

NEGATIVE_PADDING = -0.1
INVALID_PADDING = 1

NEGATIVE_IMG_SIZE = -256
FLOAT_IMG_SIZE = 256.5

VALID_PERMUTATION = [5, 2, 3, 4, 1]
# NOTE: The permutation [3, 1, 4, 2] is only invalid with respect to a card with five emojis.
INVALID_PERMUTATIONS = [
    [1, 1, 3, 4, 5],
    [1, 2, 2, 3, 4],
    [3, 1, 4, 2],
    [0, 1, 2, 3, 4]
]


@pytest.fixture
def card():
    return Card(FIVE_VALID_EMOJI_NAMES, packing="ccir")


def _all_emojis_rotated(card: Card) -> bool:
    """Check if all emojis on a card have been rotated.

    Args:
        card: The playing card to check.

    Returns:
        True if all emojis have been rotated, False otherwise.
    """

    return all(emoji.rotation != 0 for emoji in card.emojis.values())


def _no_emojis_rotated(card: Card) -> bool:
    """Check if no emojis on a card have been rotated.

    Args:
        card: The playing card to check.

    Returns:
        True if no emojis have been rotated, False otherwise.
    """

    return all(emoji.rotation == 0 for emoji in card.emojis.values())


def test_init_with_invalid_emoji_names():
    with pytest.raises(TypeError):
        Card()  # pylint: disable=no-value-for-parameter
    with pytest.raises(ValueError):
        Card([])
    with pytest.raises(ValueError):
        Card([*FIVE_VALID_EMOJI_NAMES, INVALID_EMOJI_NAME])


def test_init_with_duplicate_emoji_names():
    with pytest.warns(UserWarning):
        card = Card(FIVE_VALID_EMOJI_NAMES * 2)
    assert card.emoji_names == FIVE_VALID_EMOJI_NAMES


def test_init_with_invalid_layouts():
    # Invalid packing
    with pytest.raises(ValueError):
        Card(FIVE_VALID_EMOJI_NAMES, packing=INVALID_PACKING)

    # More than 50 emojis
    with pytest.raises(ValueError):
        Card(constants.CLASSIC_DOBBLE_EMOJIS)

    # Packings "ccib", "ccic", "ccir", and "ccis" not available for 1 to 4 emojis
    for packing, num_emojis in INVALID_LAYOUTS:
        with pytest.warns(UserWarning):
            Card(FIVE_VALID_EMOJI_NAMES[:num_emojis], packing=packing)


def test_init_with_valid_parameters(card):
    assert isinstance(card, Card)
    assert card.emoji_names == FIVE_VALID_EMOJI_NAMES
    assert card.packing == "ccir"
    assert card.rotation == 0
    assert card.num_emojis == 5
    for name in FIVE_VALID_EMOJI_NAMES:
        assert isinstance(card.emojis[name], Emoji)


def test_repr(card):
    assert repr(card) == (
        "Card data\n  Number of emojis: 5\n  Emojis: ['unicorn', 'dolphin', 'cheese wedge', "
        "'bomb', 'ice']\n  Packing: ccir\n  Rotation: 0.0 degrees"
    )


def test_get_array_with_default_parameters(card):
    returned_array = card.get_array()
    assert isinstance(returned_array, np.ndarray)
    assert returned_array.shape == (1024, 1024, 4)


def test_get_img_with_invalid_parameters(card):
    with pytest.raises(ValueError):
        card.get_img(padding=NEGATIVE_PADDING)
    with pytest.raises(ValueError):
        card.get_img(padding=INVALID_PADDING)
    with pytest.raises(ValueError):
        card.get_img(img_size=NEGATIVE_IMG_SIZE)
    with pytest.raises(ValueError):
        card.get_img(img_size=FLOAT_IMG_SIZE)


def test_get_img_with_default_parameters(card):
    returned_img = card.get_img()
    assert isinstance(returned_img, Image.Image)
    assert returned_img.size == (1024, 1024)
    assert returned_img.mode == "RGBA"


def test_get_img_with_non_default_parameters(card):
    returned_img = card.get_img(
        outline_only=True,
        padding=0.1,
        img_size=512
    )
    assert isinstance(returned_img, Image.Image)
    assert returned_img.size == (512, 512)
    assert returned_img.mode == "RGBA"


def test_get_img_with_rotation(card, mocker):
    mock_rotate = mocker.patch("PIL.Image.Image.rotate")
    card.rotate(60)
    _ = card.get_img()
    mock_rotate.assert_called_once_with(60, resample=Resampling.BICUBIC)


def test_reset_emoji_rotations_with_no_input(card):
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)
    card.reset_emoji_rotations()
    assert _no_emojis_rotated(card)


def test_reset_emoji_rotations_with_single_emoji(card):
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)
    emoji_name = FIVE_VALID_EMOJI_NAMES[3]
    card.reset_emoji_rotations(emoji_name)
    assert card.emojis[emoji_name].rotation == 0
    non_reset_emojis = [
        name for name in FIVE_VALID_EMOJI_NAMES if name != emoji_name
    ]
    for name in non_reset_emojis:
        assert card.emojis[name].rotation != 0


def test_reset_emoji_rotations_with_multiple_emojis(card):
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)
    emoji_names = [
        FIVE_VALID_EMOJI_NAMES[0],
        FIVE_VALID_EMOJI_NAMES[2],
        FIVE_VALID_EMOJI_NAMES[4]
    ]
    card.reset_emoji_rotations(emoji_names)
    for name in emoji_names:
        assert card.emojis[name].rotation == 0
    non_reset_emojis = [
        name for name in FIVE_VALID_EMOJI_NAMES if name not in emoji_names
    ]
    for name in non_reset_emojis:
        assert card.emojis[name].rotation != 0


def test_reset_emoji_rotations_with_invalid_inputs(card):
    # Invalid emoji name
    with pytest.raises(ValueError):
        card.reset_emoji_rotations(INVALID_EMOJI_NAME)

    # Emoji instead of name of emoji
    with pytest.raises(ValueError):
        card.reset_emoji_rotations(card.emojis[FIVE_VALID_EMOJI_NAMES[0]])

    # Integer instead of string or list of strings
    with pytest.raises(ValueError):
        card.reset_emoji_rotations(42)

    # List with invalid emoji name
    with pytest.raises(ValueError):
        card.reset_emoji_rotations([FIVE_VALID_EMOJI_NAMES[0], INVALID_EMOJI_NAME])

    # List of strings containing an integer
    with pytest.raises(ValueError):
        card.reset_emoji_rotations([FIVE_VALID_EMOJI_NAMES[0], 42, FIVE_VALID_EMOJI_NAMES[1]])


def test_rotate_emojis_with_no_input(card):
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)


def test_rotate_emojis_with_seed_only(card):
    card.rotate_emojis(seed=42)
    rotations = [
        card.emojis[name].rotation for name in FIVE_VALID_EMOJI_NAMES
    ]
    card.reset_emoji_rotations()
    assert _no_emojis_rotated(card)
    card.rotate_emojis(seed=42)
    for name, rotation in zip(FIVE_VALID_EMOJI_NAMES, rotations):
        assert card.emojis[name].rotation == rotation


@pytest.mark.parametrize("degrees", [45, 90, 180, -45, -90, -180])
def test_rotate_emojis_with_single_emoji(card, degrees):
    emoji_name = FIVE_VALID_EMOJI_NAMES[3]
    previous_rotation = card.emojis[emoji_name].rotation
    card.rotate_emojis((emoji_name, degrees))
    new_rotation = card.emojis[emoji_name].rotation
    assert (previous_rotation + degrees) % 360 == new_rotation
    non_rotated_emojis = [
        name for name in FIVE_VALID_EMOJI_NAMES if name != emoji_name
    ]
    for name in non_rotated_emojis:
        assert card.emojis[name].rotation == 0


def test_rotate_emojis_with_multiple_emojis(card):
    emoji_data = [
        (FIVE_VALID_EMOJI_NAMES[0], 30),
        (FIVE_VALID_EMOJI_NAMES[2], -45),
        (FIVE_VALID_EMOJI_NAMES[4], 15)
    ]
    card.rotate_emojis(emoji_data)
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[0]].rotation == 30
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[1]].rotation == 0
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[2]].rotation == 315
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[3]].rotation == 0
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[4]].rotation == 15


def test_rotate_emojis_with_invalid_inputs(card):
    # Invalid emoji name
    with pytest.raises(ValueError):
        card.rotate_emojis((INVALID_EMOJI_NAME, 30))

    # Single tuple of length 3
    with pytest.raises(ValueError):
        card.rotate_emojis((FIVE_VALID_EMOJI_NAMES[0], 30, 45))

    # List with single tuple of length 1
    with pytest.raises(ValueError):
        card.rotate_emojis([(FIVE_VALID_EMOJI_NAMES[0])])

    # List with multiple tuples, one of incorrect length
    with pytest.raises(ValueError):
        card.rotate_emojis([
            (FIVE_VALID_EMOJI_NAMES[0], 30),
            (FIVE_VALID_EMOJI_NAMES[1], 45),
            (FIVE_VALID_EMOJI_NAMES[2], 60, "incorrect_tuple")
        ])

    # String instead of tuple (i.e., only emoji name w/o rotation)
    with pytest.raises(ValueError):
        card.rotate_emojis(FIVE_VALID_EMOJI_NAMES[0])

    # Float instead of tuple (i.e., only rotation w/o emoji name)
    with pytest.raises(ValueError):
        card.rotate_emojis(30.0)


def test_show(card, mocker):
    mock_show = mocker.patch("PIL.Image.Image.show")
    card.show()
    mock_show.assert_called_once()


@pytest.mark.parametrize("invalid_permutation", INVALID_PERMUTATIONS)
def test_shuffle_emojis_with_invalid_permutations(card, invalid_permutation):
    with pytest.raises(ValueError):
        card.shuffle_emojis(permutation=invalid_permutation)


def test_shuffle_emojis_with_identity(card):
    emoji_names = card.emoji_names.copy()
    shuffled_names = card.shuffle_emojis(permutation=list(range(1, 6)))
    assert shuffled_names == emoji_names


def test_shuffle_emojis_with_valid_permutation(card):
    shuffled_names = card.shuffle_emojis(permutation=VALID_PERMUTATION)
    assert shuffled_names == FIVE_VALID_EMOJI_NAMES_SHUFFLED


def test_shuffle_emojis_without_permutation():
    card = Card(constants.CLASSIC_DOBBLE_EMOJIS[:10])
    emoji_names = card.emoji_names.copy()
    shuffled_names = card.shuffle_emojis(seed=42)
    assert shuffled_names != emoji_names
