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

NEGATIVE_IMAGE_SIZE = -256
FLOAT_IMAGE_SIZE = 256.5
VALID_IMAGE_SIZE = 256

CCI3_REL_COORDINATES = np.array([
    [-0.464101615137754587054892683011, -0.267949192431122706472553658494],
    [0.464101615137754587054892683011, -0.267949192431122706472553658494],
    [0.000000000000000000000000000000, 0.535898384862245412945107316988]
])
CCIR5_REL_COORDINATES = np.array([
    [-0.346050887765097367199182146056, -0.697732321641936395624436036149],
    [-0.075176296375555391000475331715, 0.683099132137561605481093127186],
    [0.243810256576120044094861308920, -0.566707310534312245838260639042],
    [0.515511837678785839970087098763, 0.212696996113075358075809441850],
    [-0.505456655669173835012569299809, -0.000000000000000000000000000000]
])
CCIS5_REL_COORDINATES = np.array([
    [-0.059817060736012394572641780126, -0.741684136964929306983051348505],
    [0.045118065926854828550381320779, 0.713113086130068554827617918061],
    [0.557320022845714939998766546600, 0.372560089022691612125001453910],
    [0.478020143114896574351640499785, -0.356464571708361592424519255313],
    [-0.429077903380960672427751459318, -0.000000000000000000000000000000]
])

CCI3_LARGEST_REL_RADIUS = 0.464101615137754587054892683012
CCIR5_LARGEST_REL_RADIUS = 0.494543344330826164987430700191
CCIS5_LARGEST_REL_RADIUS = 0.570922096619039327572248540682

CCI3_REL_RADII = np.array([
    0.464101615137754587054892683012,
    0.464101615137754587054892683012,
    0.464101615137754587054892683012
])
CCIR5_REL_RADII = np.array([
    0.22116650714876250,
    0.31277667395246600,
    0.38307162731420190,
    0.44233301429752500,
    0.49454334433082614
])
CCIS5_REL_RADII = np.array([
    0.25532412357937495,
    0.28546104830951970,
    0.32962202616930790,
    0.40370288604856400,
    0.57092209661903940
])

# Based on an image size of 256x256 (cf. VALID_IMAGE_SIZE above)
CCI3_COORDINATES = np.array([
    [68,  93],
    [187,  93],
    [128, 196]
])
CCIR5_COORDINATES = np.array([
    [83, 38],
    [118, 215],
    [159, 55],
    [193, 155],
    [63, 128]
])
CCIS5_COORDINATES = np.array([
    [120, 33],
    [133, 219],
    [199, 175],
    [189, 82],
    [73, 128]
])

# Based on an image size of 256x256 (cf. VALID_IMAGE_SIZE above)
CCI3_RADII = np.array([118, 118, 118])
CCIR5_RADII = np.array([56, 80, 98, 113, 126])
CCIS5_RADII = np.array([65, 73, 84, 103, 146])


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
        packing._read_coordinates_from_file(*VALID_COMBO_CCI), CCI3_REL_COORDINATES
    )


def test_read_coordinates_from_file_with_valid_combo_ccir():
    np.testing.assert_array_equal(
        packing._read_coordinates_from_file(*VALID_COMBO_CCIR), CCIR5_REL_COORDINATES
    )


def test_read_coordinates_from_file_with_valid_combo_ccis():
    np.testing.assert_array_equal(
        packing._read_coordinates_from_file(*VALID_COMBO_CCIS), CCIS5_REL_COORDINATES
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
    assert packing._read_radius_from_file(*VALID_COMBO_CCI) == CCI3_LARGEST_REL_RADIUS


def test_read_radius_from_file_with_valid_combo_ccir():
    assert packing._read_radius_from_file(*VALID_COMBO_CCIR) == CCIR5_LARGEST_REL_RADIUS


def test_read_radius_from_file_with_valid_combo_ccis():
    assert packing._read_radius_from_file(*VALID_COMBO_CCIS) == CCIS5_LARGEST_REL_RADIUS


def test_compute_radii_with_negative_num_circles():
    with pytest.raises(ValueError):
        packing._compute_radii(NEGATIVE_NUM_CIRCLES, VALID_PACKING_TYPE, CCI3_LARGEST_REL_RADIUS)


def test_compute_radii_with_float_num_circles():
    with pytest.raises(ValueError):
        packing._compute_radii(FLOAT_NUM_CIRCLES, VALID_PACKING_TYPE, CCI3_LARGEST_REL_RADIUS)


def test_compute_radii_with_invalid_packing_type():
    with pytest.raises(ValueError):
        packing._compute_radii(VALID_NUM_CIRCLES, INVALID_PACKING_TYPE, CCI3_LARGEST_REL_RADIUS)


def test_compute_radii_with_negative_radius():
    with pytest.raises(ValueError):
        packing._compute_radii(*VALID_COMBO_CCI, -CCI3_LARGEST_REL_RADIUS)


def test_compute_radii_with_zero_radius():
    with pytest.raises(ValueError):
        packing._compute_radii(*VALID_COMBO_CCI, 0)


def test_compute_radii_with_invalid_radius():
    with pytest.raises(ValueError):
        packing._compute_radii(*VALID_COMBO_CCI, CCI3_LARGEST_REL_RADIUS + 1)


def test_compute_radii_with_valid_parameters_cci():
    np.testing.assert_array_equal(
        packing._compute_radii(*VALID_COMBO_CCI, CCI3_LARGEST_REL_RADIUS), CCI3_REL_RADII
    )


def test_compute_radii_with_valid_parameters_ccir():
    np.testing.assert_array_equal(
        packing._compute_radii(*VALID_COMBO_CCIR, CCIR5_LARGEST_REL_RADIUS), CCIR5_REL_RADII
    )


def test_compute_radii_with_valid_parameters_ccis():
    np.testing.assert_array_equal(
        packing._compute_radii(*VALID_COMBO_CCIS, CCIS5_LARGEST_REL_RADIUS), CCIS5_REL_RADII
    )


def test_convert_coordinates_to_pixels_with_invalid_coordinates():
    with pytest.raises(ValueError):
        packing._convert_coordinates_to_pixels(CCI3_REL_COORDINATES + 1, VALID_IMAGE_SIZE)


def test_convert_coordinates_to_pixels_with_float_image_size():
    with pytest.raises(ValueError):
        packing._convert_coordinates_to_pixels(CCI3_REL_COORDINATES, FLOAT_IMAGE_SIZE)


def test_convert_coordinates_to_pixels_with_negative_image_size():
    with pytest.raises(ValueError):
        packing._convert_coordinates_to_pixels(CCI3_REL_COORDINATES, NEGATIVE_IMAGE_SIZE)


def test_convert_coordinates_to_pixels_with_valid_parameters_cci():
    np.testing.assert_array_equal(
        packing._convert_coordinates_to_pixels(CCI3_REL_COORDINATES, VALID_IMAGE_SIZE),
        CCI3_COORDINATES
    )


def test_convert_coordinates_to_pixels_with_valid_parameters_ccir():
    np.testing.assert_array_equal(
        packing._convert_coordinates_to_pixels(CCIR5_REL_COORDINATES, VALID_IMAGE_SIZE),
        CCIR5_COORDINATES
    )


def test_convert_coordinates_to_pixels_with_valid_parameters_ccis():
    np.testing.assert_array_equal(
        packing._convert_coordinates_to_pixels(CCIS5_REL_COORDINATES, VALID_IMAGE_SIZE),
        CCIS5_COORDINATES
    )


def test_convert_radii_to_pixels_with_invalid_radii():
    with pytest.raises(ValueError):
        packing._convert_radii_to_pixels(CCI3_REL_RADII + 1, VALID_IMAGE_SIZE)


def test_convert_radii_to_pixels_with_float_image_size():
    with pytest.raises(ValueError):
        packing._convert_radii_to_pixels(CCI3_REL_RADII, FLOAT_IMAGE_SIZE)


def test_convert_radii_to_pixels_with_negative_image_size():
    with pytest.raises(ValueError):
        packing._convert_radii_to_pixels(CCI3_REL_RADII, NEGATIVE_IMAGE_SIZE)


def test_convert_radii_to_pixels_with_valid_parameters_cci():
    np.testing.assert_array_equal(
        packing._convert_radii_to_pixels(CCI3_REL_RADII, VALID_IMAGE_SIZE),
        CCI3_RADII
    )


def test_convert_radii_to_pixels_with_valid_parameters_ccir():
    np.testing.assert_array_equal(
        packing._convert_radii_to_pixels(CCIR5_REL_RADII, VALID_IMAGE_SIZE),
        CCIR5_RADII
    )


def test_convert_radii_to_pixels_with_valid_parameters_ccis():
    np.testing.assert_array_equal(
        packing._convert_radii_to_pixels(CCIS5_REL_RADII, VALID_IMAGE_SIZE),
        CCIS5_RADII
    )
