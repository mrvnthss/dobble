# pylint: disable=missing-function-docstring, missing-module-docstring

import pytest

from dobble import constants
from dobble import Card, Emoji


INVALID_EMOJI_NAME = "invalid emoji name"
FIVE_VALID_EMOJI_NAMES = [
    "unicorn",
    "dolphin",
    "cheese wedge",
    "bomb",
    "ice"
]
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


def test_card_init_with_invalid_emoji_name():
    with pytest.raises(ValueError):
        Card([INVALID_EMOJI_NAME])


def test_card_init_with_empty_emoji_names():
    with pytest.raises(ValueError):
        Card([])


def test_card_init_with_duplicate_emoji_names():
    with pytest.warns(UserWarning):
        card = Card(FIVE_VALID_EMOJI_NAMES * 2)
    assert card.emoji_names == FIVE_VALID_EMOJI_NAMES


def test_card_init_with_invalid_layouts():
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


def test_card_init_with_valid_emojis():
    card = Card(FIVE_VALID_EMOJI_NAMES, packing="ccir")
    assert card.emoji_names == FIVE_VALID_EMOJI_NAMES
    assert card.rotation == 0
    assert card.packing == "ccir"
    assert card.num_emojis == 5
    for name in FIVE_VALID_EMOJI_NAMES:
        assert isinstance(card.emojis[name], Emoji)


def test_card_get_img_with_negative_padding():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    with pytest.raises(ValueError):
        card.get_img(padding=NEGATIVE_PADDING)


def test_card_get_img_with_invalid_padding():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    with pytest.raises(ValueError):
        card.get_img(padding=INVALID_PADDING)


def test_card_get_img_with_negative_img_size():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    with pytest.raises(ValueError):
        card.get_img(img_size=NEGATIVE_IMG_SIZE)


def test_card_get_img_with_float_img_size():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    with pytest.raises(ValueError):
        card.get_img(img_size=FLOAT_IMG_SIZE)


def test_card_get_img_with_bw_img():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    returned_img = card.get_img(outline_only=True, img_size=512)

    assert returned_img.mode == "RGBA"
    assert returned_img.size == (512, 512)


def test_card_get_img_with_color_img():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    returned_img = card.get_img(outline_only=False, img_size=1024)

    assert returned_img.mode == "RGBA"
    assert returned_img.size == (1024, 1024)


def test_card_reset_emoji_rotation():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    emoji_name = FIVE_VALID_EMOJI_NAMES[2]
    card.rotate_emoji(emoji_name, -70)
    assert card.emojis[emoji_name].rotation == 290
    card.reset_emoji_rotation(emoji_name)
    assert card.emojis[emoji_name].rotation == 0


def test_card_reset_rotation():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.rotate(-70)
    assert card.rotation == 290
    card.reset_rotation()
    assert card.rotation == 0


def test_card_rotate():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.rotate(30)
    assert card.rotation == 30
    card.rotate(-45)
    assert card.rotation == 345
    card.rotate(15)
    assert card.rotation == 0


def test_card_rotate_emoji():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    emoji_name = FIVE_VALID_EMOJI_NAMES[3]
    card.rotate_emoji(emoji_name, 30)
    assert card.emojis[emoji_name].rotation == 30
    card.rotate_emoji(emoji_name, -45)
    assert card.emojis[emoji_name].rotation == 345
    card.rotate_emoji(emoji_name, 15)
    assert card.emojis[emoji_name].rotation == 0
    for name in FIVE_VALID_EMOJI_NAMES:
        if name != emoji_name:
            assert card.emojis[name].rotation == 0


def test_card_shuffle_emojis_with_invalid_permutations():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    for invalid_permutation in INVALID_PERMUTATIONS:
        with pytest.raises(ValueError):
            card.shuffle_emojis(permutation=invalid_permutation)


def test_card_shuffle_emojis_with_identity():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    emoji_names = card.emoji_names.copy()
    card.shuffle_emojis(permutation=list(range(1, 6)))
    assert card.emoji_names == emoji_names


def test_card_shuffle_emojis_with_valid_permutation():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.shuffle_emojis(permutation=VALID_PERMUTATION)
    assert card.emoji_names == FIVE_VALID_EMOJI_NAMES_SHUFFLED


def test_card_shuffle_emojis_without_permutation():
    card = Card(constants.CLASSIC_DOBBLE_EMOJIS[:10])
    emoji_names = card.emoji_names.copy()
    card.shuffle_emojis(seed=42)
    assert card.emoji_names != emoji_names
