"""This script sets up the OpenMoji data used in the dobble package.

Typical usage example:

  >>> python setup_openmoji.py
"""


import json
import shutil
from collections import defaultdict
from pathlib import Path

import requests

from dobble import constants


# Constants controlling which tasks to perform
DOWNLOAD_EXTRACT_AND_ORGANIZE = False
FIND_DUPLICATES = False
REMOVE_DUPLICATES = True
RESTRUCTURE_JSON_FILE = True

# OpenMoji data
OPENMOJI_DIR = Path("data/openmoji")
OPENMOJI_JSON = OPENMOJI_DIR / "openmoji.json"

# OpenMoji emojis whose "annotations" parameter is not unique
DUPLICATES = [
    ("E319", "extras-openmoji"),       # brain
    ("E001", "extras-openmoji"),       # donkey
    ("E011", "extras-openmoji"),       # microbe
    ("E0C3", "extras-openmoji"),       # pretzel
    ("E1D1", "extras-openmoji"),       # keyboard
    ("E104", "extras-openmoji"),       # scroll
    ("E347", "extras-openmoji"),       # axe
    ("E269", "extras-openmoji"),       # link
    ("E204", "extras-openmoji"),       # elevator
    ("E216", "extras-openmoji"),       # moai
    ("1F3F3-FE0F", "extras-openmoji")  # white flag
]


def download_and_extract_openmoji_data() -> None:
    """Download and extract OpenMoji data from GitHub."""

    # Remove OpenMoji data directory if it exists
    if OPENMOJI_DIR.exists():
        shutil.rmtree(OPENMOJI_DIR)

    # Re-create OpenMoji data directory
    OPENMOJI_DIR.mkdir(parents=True)

    # URLs and corresponding file names of OpenMoji data
    urls = [
        constants.OPENMOJI_LICENSE_URL,
        constants.OPENMOJI_JSON_URL,
        constants.OPENMOJI_COLOR_URL,
        constants.OPENMOJI_BLACK_URL
    ]
    file_names = [
        "LICENSE.txt",
        "openmoji.json",
        "color.zip",
        "black.zip"
    ]
    paths = [OPENMOJI_DIR / file_name for file_name in file_names]

    # Download files and save to OpenMoji data directory
    for url, path in zip(urls, paths):
        response = requests.get(url, timeout=10)
        with open(path, mode="wb") as file:
            file.write(response.content)

        # Extract zip archives
        if path.suffix == ".zip":
            shutil.unpack_archive(path, extract_dir=path.with_suffix(""))
            path.unlink()


def organize_openmoji_data() -> None:
    """Organize OpenMoji emojis into subdirectories.

    This function organizes the OpenMoji emojis into subdirectories
    based on their "group" attribute in the JSON file provided by
    OpenMoji.
    """

    # Read JSON file provided by OpenMoji
    with OPENMOJI_JSON.open("r", encoding="utf-8") as json_file:
        openmoji_data = json.load(json_file)

    # Create subdirectory for each unique "group" value
    unique_groups = set(emoji["group"] for emoji in openmoji_data)
    for group in unique_groups:
        (OPENMOJI_DIR / "black" / group).mkdir(parents=True, exist_ok=True)
        (OPENMOJI_DIR / "color" / group).mkdir(parents=True, exist_ok=True)

    # Move emojis to their respective "group" directories
    for entry in openmoji_data:
        group = entry["group"]
        hexcode = entry["hexcode"]

        for mode in ["black", "color"]:
            emoji_fpath = OPENMOJI_DIR / mode / f"{hexcode}.png"
            if emoji_fpath.exists():
                target_dir = OPENMOJI_DIR / mode / group
                shutil.move(str(emoji_fpath), str(target_dir))


def find_duplicates() -> dict[str, list[dict[str, str]]]:
    """Find emojis with duplicate annotations.

    This function finds emojis from the OpenMoji dataset that have a
    non-unique "annotation" in the JSON file provided by OpenMoji.

    Returns:
        A dictionary of emojis from the OpenMoji dataset that have a
        non-unique "annotation" in the JSON file provided by OpenMoji.
        The dictionary is indexed by the "annotation" and contains a
        list of dictionaries of the emojis with that annotation.  Each
        dictionary contains the "hexcode" and "group" of the emoji.
    """

    # Read JSON file provided by OpenMoji
    with OPENMOJI_JSON.open("r", encoding="utf-8") as json_file:
        openmoji_data = json.load(json_file)

    # Count the number of appearances of each annotation
    annotation_counts = defaultdict(int)
    for entry in openmoji_data:
        annotation_counts[entry["annotation"]] += 1

    # Collect emojis with duplicate annotations
    duplicates = defaultdict(list)
    for entry in openmoji_data:
        if annotation_counts[entry["annotation"]] > 1:
            emoji_data = {
                "hexcode": entry["hexcode"],
                "group": entry["group"]
            }
            duplicates[entry["annotation"]].append(emoji_data)

    return duplicates


def print_duplicates(duplicates: dict[str, list[dict[str, str]]]) -> None:
    """Print emojis with duplicate annotations.

    This function prints emojis from the OpenMoji dataset that have a
    non-unique "annotation" in the JSON file provided by OpenMoji.  It
    prints the annotations along with the hexcodes and groups of all
    emojis with that annotation.

    Args:
        duplicates: A dictionary of emojis from the OpenMoji dataset
          that have a non-unique "annotation" in the JSON file provided
          by OpenMoji as returned by the ``find_duplicates`` function.
    """

    for annotation, emoji_data in duplicates.items():
        print(f"Annotation: {annotation}")
        for entry in emoji_data:
            print(f'\t("{entry["hexcode"]}", "{entry["group"]}")')
        print()


def remove_duplicates() -> None:
    """Remove OpenMoji emojis w/ non-unique "annotation" parameter.

    This function removes emojis from the OpenMoji dataset that have a
    non-unique "annotation" by deleting the emoji image as well as the
    corresponding entry in the JSON file.  Duplicates are identified via
    the ``DUPLICATES`` list.
    """

    for hexcode, group in DUPLICATES:
        # Construct file paths for both outline-only and color versions
        black_fpath = OPENMOJI_DIR / "black" / group / f"{hexcode}.png"
        color_fpath = OPENMOJI_DIR / "color" / group / f"{hexcode}.png"

        # Remove emoji images (outline-only and color) if they exist
        black_fpath.unlink(missing_ok=True)
        color_fpath.unlink(missing_ok=True)

    # Read JSON file provided by OpenMoji
    with OPENMOJI_JSON.open("r", encoding="utf-8") as json_file:
        openmoji_data = json.load(json_file)

    # Remove entries corresponding to duplicates
    openmoji_data = [
        entry for entry in openmoji_data if (entry["hexcode"], entry["group"]) not in DUPLICATES
    ]

    # Write updated data back to JSON file
    with OPENMOJI_JSON.open("w", encoding="utf-8") as json_file:
        json.dump(openmoji_data, json_file, indent=2, ensure_ascii=False)


def restructure_json_file() -> None:
    """Restructure OpenMoji JSON file.

    This function restructures the JSON file provided by OpenMoji in
    such a way that the JSON file contains a dictionary with the emoji
    "annotation" as keys and dictionaries containing the "hexcode",
    "group", and "subgroups" parameters as values.
    """

    # Read JSON file provided by OpenMoji
    with OPENMOJI_JSON.open("r", encoding="utf-8") as json_file:
        openmoji_data = json.load(json_file)

    # Create dictionary with desired format
    restructured_data = {}
    for entry in openmoji_data:
        key = entry["annotation"]
        restructured_data[key] = {
            "hexcode": entry["hexcode"],
            "group": entry["group"],
            "subgroup": entry["subgroups"]
        }

    # Write restructured data to JSON file
    restructured_json_fpath = OPENMOJI_DIR / "openmoji_restructured.json"
    with restructured_json_fpath.open("w", encoding="utf-8") as json_file:
        json.dump(restructured_data, json_file, indent=4)


if __name__ == "__main__":
    if DOWNLOAD_EXTRACT_AND_ORGANIZE:
        download_and_extract_openmoji_data()
        organize_openmoji_data()

    if FIND_DUPLICATES:
        duplicate_annotations = find_duplicates()
        print_duplicates(duplicate_annotations)

    if REMOVE_DUPLICATES:
        remove_duplicates()

    if RESTRUCTURE_JSON_FILE:
        restructure_json_file()
