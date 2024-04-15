# pylint: disable=protected-access, missing-function-docstring

"""Unit tests for the "packing" module of the "dobble" package."""

# Third-Party Library Imports
import numpy as np
import pytest

# Local Imports
from dobble import constants
from dobble import packing


# Constants for Testing
INVALID_PACKING_TYPE = "ccid"
VALID_PACKING_TYPE = "ccir"

NEGATIVE_NUM_CIRCLES = -7
FLOAT_NUM_CIRCLES = 7.5
VALID_NUM_CIRCLES = 5

INVALID_COMBO = (4, "ccir")
VALID_COMBO = (3, "cci")

CCI3_COORDINATES = np.array(
    [[-0.464101615137754587054892683011, -0.267949192431122706472553658494],
     [0.464101615137754587054892683011, -0.267949192431122706472553658494],
     [0.000000000000000000000000000000, 0.535898384862245412945107316988]]
)
CCI3_RADIUS = 0.464101615137754587054892683012


def test_is_valid_packing_type_with_invalid_packing_type():
    assert not packing._is_valid_packing_type(INVALID_PACKING_TYPE)


def test_is_valid_packing_type_with_valid_packing_types():
    for packing_type in constants.PACKING_TYPES_DICT:
        assert packing._is_valid_packing_type(packing_type)


def test_read_coordinates_from_file_with_negative_num_circles():
    with pytest.raises(ValueError):
        packing._read_coordinates_from_file(NEGATIVE_NUM_CIRCLES, VALID_PACKING_TYPE)


def test_read_coordinates_from_file_with_float_num_circles():
    with pytest.raises(ValueError):
        packing._read_coordinates_from_file(FLOAT_NUM_CIRCLES, VALID_PACKING_TYPE)


def test_read_coordinates_from_file_with_invalid_packing_type():
    with pytest.raises(ValueError):
        packing._read_coordinates_from_file(VALID_NUM_CIRCLES, INVALID_PACKING_TYPE)


def test_read_coordinates_from_file_with_invalid_combo():
    with pytest.raises(FileNotFoundError):
        packing._read_coordinates_from_file(*INVALID_COMBO)


def test_read_coordinates_from_file_with_valid_combo():
    np.testing.assert_array_equal(
        packing._read_coordinates_from_file(*VALID_COMBO), CCI3_COORDINATES
    )


def test_read_radius_from_file_with_negative_num_circles():
    with pytest.raises(ValueError):
        packing._read_radius_from_file(NEGATIVE_NUM_CIRCLES, VALID_PACKING_TYPE)


def test_read_radius_from_file_with_float_num_circles():
    with pytest.raises(ValueError):
        packing._read_radius_from_file(FLOAT_NUM_CIRCLES, VALID_PACKING_TYPE)


def test_read_radius_from_file_with_invalid_packing_type():
    with pytest.raises(ValueError):
        packing._read_radius_from_file(VALID_NUM_CIRCLES, INVALID_PACKING_TYPE)


def test_read_radius_from_file_with_invalid_combo():
    with pytest.raises(ValueError):
        packing._read_radius_from_file(*INVALID_COMBO)


def test_read_radius_from_file_with_valid_combo():
    assert packing._read_radius_from_file(*VALID_COMBO) == CCI3_RADIUS
