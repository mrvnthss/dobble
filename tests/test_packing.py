# pylint: disable=protected-access, missing-function-docstring, missing-module-docstring

import numpy as np
import pytest

from dobble import constants
from dobble import packing


INVALID_PACKING_TYPE = "ccid"
VALID_PACKING_TYPE = "ccir"

NEGATIVE_NUM_CIRCLES = -7
FLOAT_NUM_CIRCLES = 7.5
VALID_NUM_CIRCLES = 5

INVALID_COMBO = (4, "ccir")
VALID_COMBO_CCI = (3, "cci")
VALID_COMBO_CCIR = (5, "ccir")
VALID_COMBO_CCIS = (5, "ccis")

CCI3_COORDINATES = np.array([
    [-0.464101615137754587054892683011, -0.267949192431122706472553658494],
    [0.464101615137754587054892683011, -0.267949192431122706472553658494],
    [0.000000000000000000000000000000, 0.535898384862245412945107316988]
])
CCIR5_COORDINATES = np.array([
    [-0.346050887765097367199182146056, -0.697732321641936395624436036149],
    [-0.075176296375555391000475331715, 0.683099132137561605481093127186],
    [0.243810256576120044094861308920, -0.566707310534312245838260639042],
    [0.515511837678785839970087098763, 0.212696996113075358075809441850],
    [-0.505456655669173835012569299809, -0.000000000000000000000000000000]
])

CCI3_LARGEST_RADIUS = 0.464101615137754587054892683012
CCIR5_LARGEST_RADIUS = 0.494543344330826164987430700191
CCIS5_LARGEST_RADIUS = 0.570922096619039327572248540682

CCIR5_RADII = np.array([
    0.22116650714876250,
    0.31277667395246600,
    0.38307162731420190,
    0.44233301429752500,
    0.49454334433082614
])
CCIS5_RADII = np.array([
    0.25532412357937495,
    0.28546104830951970,
    0.32962202616930790,
    0.40370288604856400,
    0.57092209661903940
])


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


def test_read_coordinates_from_file_with_valid_combo_cci():
    np.testing.assert_array_equal(
        packing._read_coordinates_from_file(*VALID_COMBO_CCI), CCI3_COORDINATES
    )


def test_read_coordinates_from_file_with_valid_combo_ccir():
    np.testing.assert_array_equal(
        packing._read_coordinates_from_file(*VALID_COMBO_CCIR), CCIR5_COORDINATES
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


def test_read_radius_from_file_with_valid_combo_cci():
    assert packing._read_radius_from_file(*VALID_COMBO_CCI) == CCI3_LARGEST_RADIUS


def test_read_radius_from_file_with_valid_combo_ccir():
    assert packing._read_radius_from_file(*VALID_COMBO_CCIR) == CCIR5_LARGEST_RADIUS


def test_compute_radii_with_negative_num_circles():
    with pytest.raises(ValueError):
        packing._compute_radii(NEGATIVE_NUM_CIRCLES, VALID_PACKING_TYPE, CCI3_LARGEST_RADIUS)


def test_compute_radii_with_float_num_circles():
    with pytest.raises(ValueError):
        packing._compute_radii(FLOAT_NUM_CIRCLES, VALID_PACKING_TYPE, CCI3_LARGEST_RADIUS)


def test_compute_radii_with_invalid_packing_type():
    with pytest.raises(ValueError):
        packing._compute_radii(VALID_NUM_CIRCLES, INVALID_PACKING_TYPE, CCI3_LARGEST_RADIUS)


def test_compute_radii_with_negative_radius():
    with pytest.raises(ValueError):
        packing._compute_radii(VALID_NUM_CIRCLES, VALID_PACKING_TYPE, -CCI3_LARGEST_RADIUS)


def test_compute_radii_with_zero_radius():
    with pytest.raises(ValueError):
        packing._compute_radii(VALID_NUM_CIRCLES, VALID_PACKING_TYPE, 0)


def test_compute_radii_with_invalid_radius():
    with pytest.raises(ValueError):
        packing._compute_radii(VALID_NUM_CIRCLES, VALID_PACKING_TYPE, CCI3_LARGEST_RADIUS + 1)


def test_compute_radii_with_valid_parameters_cci():
    radii = packing._compute_radii(*VALID_COMBO_CCI, CCI3_LARGEST_RADIUS)
    assert all(r == CCI3_LARGEST_RADIUS for r in radii)


def test_compute_radii_with_valid_parameters_ccir():
    np.testing.assert_array_equal(
        packing._compute_radii(*VALID_COMBO_CCIR, CCIR5_LARGEST_RADIUS), CCIR5_RADII
    )


def test_compute_radii_with_valid_parameters_ccis():
    np.testing.assert_array_equal(
        packing._compute_radii(*VALID_COMBO_CCIS, CCIS5_LARGEST_RADIUS), CCIS5_RADII
    )
