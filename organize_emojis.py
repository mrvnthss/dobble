# Standard Library Imports
import os
import json
import shutil

# Local Imports
from dobble import constants


def organize_emojis(directory: str) -> None:
    """Organize emojis into subdirectories based on their OpenMoji 'group' attribute.

    Args:
        directory (str): The initial subdirectory containing the emojis.  Either 'color' or 'black'.

    Returns:
        None
    """
    # Read JSON file provided by OpenMoji
    with open(constants.OPENMOJI_JSON, 'r') as json_file:
        emojis_data = json.load(json_file)

    # Obtain unique 'group' values
    groups = set(emoji['group'] for emoji in emojis_data)

    # Construct source directory path
    source_dir = os.path.join(constants.EMOJIS_DIR, directory)

    # Create subdirectory for each 'group' value
    for group in groups:
        os.makedirs(os.path.join(source_dir, group), exist_ok=True)

    # Move emojis to their respective directories
    for emoji in emojis_data:
        group = emoji['group']
        hexcode = emoji['hexcode']

        # Define source path of emoji
        source_path = os.path.join(source_dir, f"{hexcode}.png")

        # Check if the emoji exists, then move it
        if os.path.exists(source_path):
            target_dir = os.path.join(source_dir, group)
            shutil.move(source_path, target_dir)


def is_emojis_organized() -> bool:
    """Check if emojis have been organized into subdirectories.

    Returns:
        bool: True if emojis have been organized, False otherwise.
    """
    return os.path.exists(constants.EMOJIS_ORGANIZED_FLAG)
