"""This script removes emojis with non-unique annotations.

This script removes emojis from the OpenMoji dataset that have a
non-unique "annotation" by deleting the emoji image as well as the
corresponding entry in the JSON file.  Duplicates are identified by the
`DUPLICATES` list.

Typical usage example:

  python find_duplicates.py
"""


import json
from pathlib import Path


# The following emojis from the OpenMoji dataset have a non-unique annotation.
# They can be identified by running the `find_duplicates.py` script.
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

OPENMOJI = Path("data/openmoji")
OPENMOJI_JSON = OPENMOJI / "openmoji.json"


def remove_duplicates() -> None:
    """Remove emojis w/ non-unique annotation from the OpenMoji dataset.

    This function removes emojis from the OpenMoji dataset that have a
    non-unique "annotation" by deleting the emoji image as well as the
    corresponding entry in the JSON file.  Duplicates are identified by
    the `DUPLICATES` list.
    """

    # Remove duplicates from the OpenMoji dataset
    for hexcode, group in DUPLICATES:
        # Construct file paths for both color and black versions
        color_path = OPENMOJI / "color" / group / f"{hexcode}.png"
        black_path = OPENMOJI / "black" / group / f"{hexcode}.png"

        # Remove emoji images (color and black & white) if they exist
        color_path.unlink(missing_ok=True)
        black_path.unlink(missing_ok=True)

    # Update JSON file (i.e., remove entries corresponding to duplicates)
    # Read JSON file provided by OpenMoji
    with OPENMOJI_JSON.open("r", encoding="utf-8") as json_file:
        emojis_data = json.load(json_file)

    # Remove entries corresponding to duplicates
    emojis_data = [
        emoji for emoji in emojis_data if (emoji["hexcode"], emoji["group"]) not in DUPLICATES
    ]

    # Write updated data back to JSON file
    with OPENMOJI_JSON.open("w", encoding="utf-8") as json_file:
        json.dump(emojis_data, json_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    remove_duplicates()
