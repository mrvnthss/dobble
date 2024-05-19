"""This script organizes the OpenMoji emojis into subdirectories.

This script reads the JSON file provided by OpenMoji and organizes the
emojis into subdirectories based on their "group" attribute in the JSON
file.

Typical usage example:

  python organize_emojis.py
"""


import json
import shutil
from pathlib import Path


OPENMOJI_JSON = Path("data/openmoji/openmoji.json")


def organize_emojis(directory: str) -> None:
    """Organize OpenMoji emojis into subdirectories.

    This function organizes the OpenMoji emojis into subdirectories
    based on their "group" attribute in the JSON file provided by
    OpenMoji.

    Args:
        directory: The initial subdirectory containing the emojis.
          Either "color" or "black".
    """
    # Read JSON file provided by OpenMoji
    with OPENMOJI_JSON.open("r", encoding="utf-8") as json_file:
        emojis_data = json.load(json_file)

    # Obtain unique "group" values
    groups = set(emoji["group"] for emoji in emojis_data)

    # Construct source directory path
    source_dir = OPENMOJI_JSON.parent / directory

    # Create subdirectory for each "group" value
    for group in groups:
        (source_dir / group).mkdir(parents=True, exist_ok=True)

    # Move emojis to their respective directories
    for emoji in emojis_data:
        group = emoji["group"]
        hexcode = emoji["hexcode"]

        # Define source path of emoji
        source_path = source_dir / f"{hexcode}.png"

        # Check if the emoji exists, then move it
        if source_path.exists():
            target_dir = source_dir / group
            shutil.move(str(source_path), str(target_dir))


if __name__ == "__main__":
    organize_emojis("color")
    organize_emojis("black")
