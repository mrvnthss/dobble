"""Project-level constants.

Constants:
    OPENMOJI_DIR: The directory where OpenMoji emojis are stored.
    PACKINGS_DIR: The directory where data on circle packings is stored.
    RADIUS_FILE: The name of the text file containing the radius of the
      largest circle of each packing.
    OPENMOJI_LICENSE_URL: The URL of the OpenMoji license.
    OPENMOJI_JSON_URL: The URL of the OpenMoji JSON file.
    OPENMOJI_COLOR_URL: The URL of the OpenMoji color emojis.
    OPENMOJI_BLACK_URL: The URL of the OpenMoji black-and-white emojis.
    PACKINGS_DICT: A dictionary mapping packings to their associated
      radii functions.
    CLASSIC_DOBBLE_EMOJIS: A list of OpenMoji emojis to resemble the
      classic Dobble game.
    FPP_KERNELS: A dictionary of kernels of incidence matrices of finite
      projective planes whose order is a prime power.
"""


import numpy as np


# Directories and files
OPENMOJI_DIR = "data.openmoji"
PACKINGS_DIR = "data.packings"
RADIUS_FILE = "radius.txt"

# OpenMoji URLs (Release 15.0.0)
_RELEASE_SHA = "13942cdd65134df8899ed5df62ccf47b36d643d7"
_RAW_URL = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/" + _RELEASE_SHA + "/"
_DOWNLOAD_URL = "https://github.com/hfg-gmuend/openmoji/releases/download/15.0.0/"
OPENMOJI_LICENSE_URL = _RAW_URL + "LICENSE.txt"
OPENMOJI_JSON_URL = _RAW_URL + "data/openmoji.json"
OPENMOJI_COLOR_URL = _DOWNLOAD_URL + "openmoji-618x618-color.zip"
OPENMOJI_BLACK_URL = _DOWNLOAD_URL + "openmoji-618x618-black.zip"

# Available packings and their radii functions
PACKINGS_DICT = {
    "cci": lambda n: 1,
    "ccib": lambda n: n ** (-1 / 5),
    "ccic": lambda n: n ** (-2 / 3),
    "ccir": lambda n: n ** (1 / 2),
    "ccis": lambda n: n ** (-1 / 2)
}

# OpenMoji emojis that (somewhat closely) resemble the classic Dobble game
CLASSIC_DOBBLE_EMOJIS = [
    "anchor",
    "baby bottle",
    "bomb",
    "cactus",
    "candle",
    "carrot",
    "cheese wedge",
    "chess pawn",
    "classical building",
    "clown face",
    "deciduous tree",
    "dog face",
    "dolphin",
    "dragon",
    "droplet",
    "eye",
    "fire",
    "four leaf clover",
    "front-facing baby chick",
    "ghost",
    "gps",
    "green apple",
    "grinning cat with smiling eyes",
    "hammer",
    "hand with fingers splayed",
    "high voltage",
    "ice",
    "intricate",
    "lady beetle",
    "last quarter moon face",
    "light bulb",
    "locked",
    "maple leaf",
    "mouth",
    "musical score",
    "no entry",
    "old key",
    "oncoming taxi",
    "pencil",
    "person standing",
    "red exclamation mark",
    "red heart",
    "red question mark",
    "rosette",
    "scissors",
    "skull and crossbones",
    "snowflake",
    "snowman without snow",
    "spider web",
    "spider",
    "sun",
    "sunglasses",
    "T-Rex",
    "timer",
    "turtle",
    "yin yang",
    "zebra"
]

# Kernel of incidence matrix for finite projective planes of order 4
# Based on Figure 7 of Montaron (1985)
_A = [2, 1, 4, 3]
_B = [3, 4, 1, 2]
_C = [4, 3, 2, 1]

_KERNEL_4 = np.array([
    [_A, _B, _C],
    [_B, _C, _A],
    [_C, _A, _B]
])

# Kernel of incidence matrix for finite projective planes of order 8
# Based on Section 6 of Montaron (1985)
_M1 = [2, 1, 4, 3, 6, 5, 8, 7]
_M2 = [3, 4, 1, 2, 7, 8, 5, 6]
_M3 = [4, 3, 2, 1, 8, 7, 6, 5]
_M4 = [5, 6, 7, 8, 1, 2, 3, 4]
_M5 = [6, 5, 8, 7, 2, 1, 4, 3]
_M6 = [7, 8, 5, 6, 3, 4, 1, 2]
_M7 = [8, 7, 6, 5, 4, 3, 2, 1]

_KERNEL_8 = np.array([
    [_M1, _M2, _M3, _M4, _M5, _M6, _M7],
    [_M2, _M6, _M4, _M1, _M3, _M7, _M5],
    [_M3, _M4, _M7, _M5, _M6, _M1, _M2],
    [_M4, _M1, _M5, _M3, _M7, _M2, _M6],
    [_M5, _M3, _M6, _M7, _M2, _M4, _M1],
    [_M6, _M7, _M1, _M2, _M4, _M5, _M3],
    [_M7, _M5, _M2, _M6, _M1, _M3, _M4]
])

# Dictionary collecting kernels of incidence matrices of FPPs whose order is a prime power
FPP_KERNELS = {
    4: _KERNEL_4,
    8: _KERNEL_8
}
