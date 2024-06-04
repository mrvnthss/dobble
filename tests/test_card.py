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


def _all_emojis_rotated(card: Card) -> bool:
    """Check if all emojis on a card have been rotated.

    Args:
        card (Card): The playing card to check.

    Returns:
        bool: True if all emojis have been rotated, False otherwise.
    """

    return all(emoji.rotation != 0 for emoji in card.emojis.values())


def _no_emojis_rotated(card: Card) -> bool:
    """Check if no emojis on a card have been rotated.

    Args:
        card (Card): The playing card to check.

    Returns:
        bool: True if no emojis have been rotated, False otherwise.
    """

    return all(emoji.rotation == 0 for emoji in card.emojis.values())


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

    # Check that attributes are set correctly
    assert card.emoji_names == FIVE_VALID_EMOJI_NAMES
    assert card.rotation == 0
    assert card.packing == "ccir"
    assert card.num_emojis == 5

    # Check that each emoji is an instance of the Emoji class
    for name in FIVE_VALID_EMOJI_NAMES:
        assert isinstance(card.emojis[name], Emoji)


def test_card_get_array_with_bw_img():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    returned_array = card.get_array(outline_only=True, padding=0.1, img_size=256)

    assert returned_array.shape == (256, 256, 4)


def test_card_get_array_with_color_img():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    returned_array = card.get_array(outline_only=False, padding=0.05, img_size=512)

    assert returned_array.shape == (512, 512, 4)


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


def test_card_reset_card_rotation():
    card = Card(FIVE_VALID_EMOJI_NAMES)

    # Rotate card, then reset rotation, and check that it is back to 0
    card.rotate_card(-70)
    assert card.rotation != 0
    card.reset_card_rotation()
    assert card.rotation == 0


def test_card_reset_emoji_rotations_with_no_input():
    # Create card and randomly rotate all emojis
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)

    # Reset rotations and check that they are all back to 0
    card.reset_emoji_rotations()
    assert _no_emojis_rotated(card)


def test_card_reset_emoji_rotations_with_single_emoji():
    # Create card and randomly rotate all emojis
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)

    # Reset rotation of single emoji and check that it is back to 0
    emoji_name = FIVE_VALID_EMOJI_NAMES[3]
    card.reset_emoji_rotations(emoji_name)
    assert card.emojis[emoji_name].rotation == 0

    # Check that other emojis are not affected
    for name in FIVE_VALID_EMOJI_NAMES:
        if name != emoji_name:
            assert card.emojis[name].rotation != 0


def test_card_reset_emoji_rotations_with_multiple_emojis():
    # Create card and randomly rotate all emojis
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)

    # Reset rotations of multiple emojis and check that they are back to 0
    emoji_names = [
        FIVE_VALID_EMOJI_NAMES[0],
        FIVE_VALID_EMOJI_NAMES[2],
        FIVE_VALID_EMOJI_NAMES[4]
    ]
    card.reset_emoji_rotations(emoji_names)
    for name in emoji_names:
        assert card.emojis[name].rotation == 0

    # Check that other emojis are not affected
    non_reset_emojis = [name for name in FIVE_VALID_EMOJI_NAMES if name not in emoji_names]
    for name in non_reset_emojis:
        assert card.emojis[name].rotation != 0


def test_card_reset_emoji_rotations_with_invalid_emoji_name():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    with pytest.raises(ValueError):
        card.reset_emoji_rotations(INVALID_EMOJI_NAME)


def test_card_reset_emoji_rotations_with_invalid_inputs():
    card = Card(FIVE_VALID_EMOJI_NAMES)

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


def test_card_rotate_card():
    card = Card(FIVE_VALID_EMOJI_NAMES)

    # Rotate card multiple times and check that rotation is as expected
    card.rotate_card(30)
    # (0 + 30) % 360 = 30
    assert card.rotation == 30
    card.rotate_card(-45)
    # (30 - 45) % 360 = 345
    assert card.rotation == 345
    card.rotate_card(15)
    # (345 + 15) % 360 = 0
    assert card.rotation == 0


def test_card_rotate_emojis_with_no_input():
    # Create card, randomly rotate all emojis, and check that all emojis have been rotated
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.rotate_emojis(seed=42)
    assert _all_emojis_rotated(card)


def test_card_rotate_emojis_with_seed_only():
    # Create card and randomly rotate all emojis
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.rotate_emojis(seed=42)

    # Store rotations of emojis in separate list and reset rotations
    rotations = [card.emojis[name].rotation for name in FIVE_VALID_EMOJI_NAMES]
    card.reset_emoji_rotations()
    assert _no_emojis_rotated(card)

    # Rotate emojis with same seed and check that rotations are the same
    card.rotate_emojis(seed=42)
    for name, rotation in zip(FIVE_VALID_EMOJI_NAMES, rotations):
        assert card.emojis[name].rotation == rotation


def test_card_rotate_emojis_with_single_emoji():
    # Create card and pick emoji to rotate
    card = Card(FIVE_VALID_EMOJI_NAMES)
    emoji_name = FIVE_VALID_EMOJI_NAMES[3]

    # Rotate emoji multiple times and check that rotation is as expected
    card.rotate_emojis((emoji_name, 30))
    # (0 + 30) % 360 = 30
    assert card.emojis[emoji_name].rotation == 30
    card.rotate_emojis((emoji_name, -45))
    # (30 - 45) % 360 = 345
    assert card.emojis[emoji_name].rotation == 345
    card.rotate_emojis((emoji_name, 15))
    # (345 + 15) % 360 = 0
    assert card.emojis[emoji_name].rotation == 0

    # Check that other emojis are not affected
    for name in FIVE_VALID_EMOJI_NAMES:
        if name != emoji_name:
            assert card.emojis[name].rotation == 0


def test_card_rotate_emojis_with_multiple_emojis():
    # Create card and pick emojis to rotate
    card = Card(FIVE_VALID_EMOJI_NAMES)
    emoji_data = [
        (FIVE_VALID_EMOJI_NAMES[0], 30),
        (FIVE_VALID_EMOJI_NAMES[2], -45),
        (FIVE_VALID_EMOJI_NAMES[4], 15)
    ]

    # Rotate emojis and check that rotations are as expected
    card.rotate_emojis(emoji_data)
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[0]].rotation == 30
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[2]].rotation == 315
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[4]].rotation == 15

    # Check that other emojis are not affected
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[1]].rotation == 0
    assert card.emojis[FIVE_VALID_EMOJI_NAMES[3]].rotation == 0


def test_card_rotate_emojis_with_invalid_emoji_name():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    with pytest.raises(ValueError):
        card.rotate_emojis((INVALID_EMOJI_NAME, 30))


def test_card_rotate_emojis_with_invalid_inputs():
    card = Card(FIVE_VALID_EMOJI_NAMES)

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


def test_card_show(mocker):
    mock_show = mocker.patch("PIL.Image.Image.show")
    card = Card(FIVE_VALID_EMOJI_NAMES)
    card.show()
    mock_show.assert_called_once()


def test_card_shuffle_emojis_with_invalid_permutations():
    card = Card(FIVE_VALID_EMOJI_NAMES)
    for invalid_permutation in INVALID_PERMUTATIONS:
        with pytest.raises(ValueError):
            card.shuffle_emojis(permutation=invalid_permutation)


def test_card_shuffle_emojis_with_identity():
    card = Card(FIVE_VALID_EMOJI_NAMES)

    # Store original order of emojis in separate list and "shuffle" with identity
    emoji_names = card.emoji_names.copy()
    card.shuffle_emojis(permutation=list(range(1, 6)))

    # Check that order of emojis remains unchanged
    assert card.emoji_names == emoji_names


def test_card_shuffle_emojis_with_valid_permutation():
    card = Card(FIVE_VALID_EMOJI_NAMES)

    # Shuffle emojis and check that order is as expected
    card.shuffle_emojis(permutation=VALID_PERMUTATION)
    assert card.emoji_names == FIVE_VALID_EMOJI_NAMES_SHUFFLED


def test_card_shuffle_emojis_without_permutation():
    # Create playing card with 10 emojis from the classic Dobble set
    card = Card(constants.CLASSIC_DOBBLE_EMOJIS[:10])

    # Store original order of emojis in separate list and shuffle randomly (i.e., w/o permutation)
    emoji_names = card.emoji_names.copy()
    card.shuffle_emojis(seed=42)

    # Check that order of emojis has been changed
    assert card.emoji_names != emoji_names
