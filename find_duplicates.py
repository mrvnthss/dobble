"""This script finds emojis with duplicate annotations.

This script reads the JSON file provided by OpenMoji and finds emojis
with duplicate annotations.  It then prints the duplicate annotations
along with the hexcodes and groups of the corresponding emojis.

Typical usage example:

  python find_duplicates.py
"""


from collections import defaultdict
import json
from pathlib import Path


OPENMOJI_JSON = Path("data/openmoji/openmoji.json")


def find_duplicates() -> None:
    """Find emojis with duplicate annotations.

    This function reads the JSON file provided by OpenMoji and finds
    emojis with duplicate annotations.  It then prints the duplicate
    annotations along with the hexcodes and groups of the corresponding
    emojis.
    """
    # Read JSON file provided by OpenMoji
    with OPENMOJI_JSON.open("r", encoding="utf-8") as json_file:
        emojis_data = json.load(json_file)

    # Count the number of appearances of each annotation
    annotation_counts = defaultdict(int)
    for emoji in emojis_data:
        annotation_counts[emoji["annotation"]] += 1

    # Collect emojis with duplicate annotations
    duplicates = {}
    for emoji in emojis_data:
        if annotation_counts[emoji["annotation"]] > 1:
            emoji_data = {
                "hexcode": emoji["hexcode"],
                "group": emoji["group"]
            }
            if emoji["annotation"] in duplicates:
                duplicates[emoji["annotation"]].append(emoji_data)
            else:
                duplicates[emoji["annotation"]] = [emoji_data]

    # Print emojis with duplicate annotations
    for annotation, emoji_data in duplicates.items():
        print(annotation)
        for emoji in emoji_data:
            print(f'  ("{emoji["hexcode"]}", "{emoji["group"]}")')


if __name__ == "__main__":
    find_duplicates()
