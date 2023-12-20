"""Module defining project-level constants for the 'dobble' package.

It provides names of directories and specific files used in the project.  Further, it defines a dictionary mapping
packing types to their associated radii functions.  Finally, it defines default parameters for playing cards and
decks, and a list of emojis to resemble the classic Dobble game.

Constants:
    - EMOJIS_DIR: The directory where emojis are stored.
    - PACKING_DIR: The directory where packing data files are stored.
    - OPENMOJI_JSON: The name of the JSON file containing OpenMoji data.
    - RADIUS_TXT: The name of the text file containing the radius of the largest circle in a packing.
    - PACKING_TYPES_DICT: A dictionary mapping packing types to their associated radii functions.
    - DEFAULT_CARD_PARAMS: A dictionary of default playing card parameters.
    - DEFAULT_DECK_PARAMS: A dictionary of default deck parameters.
    - CLASSIC_DOBBLE_EMOJIS: A list of emojis to resemble the classic Dobble game.
"""

# Names of directories
EMOJIS_DIR = 'data.openmoji'
PACKING_DIR = 'data.packing_data'

# Names of specific files
OPENMOJI_JSON = 'openmoji.json'
RADIUS_TXT = 'radius.txt'

# Packing types dictionary
PACKING_TYPES_DICT = {
    'cci': (lambda n: 1, 'increasing'),
    'ccib': (lambda n: n ** (-1 / 5), 'decreasing'),
    'ccic': (lambda n: n ** (-2 / 3), 'decreasing'),
    'ccir': (lambda n: n ** (1/2), 'increasing'),
    'ccis': (lambda n: n ** (-1/2), 'decreasing')
}

# Default playing card parameters
DEFAULT_CARD_PARAMS = {
    'size': 1024,
    'packing': None,
    'padding': 0.1
}

# Default deck parameters
DEFAULT_DECK_PARAMS = {
    'name': 'my-dobble-deck',
    'emojis_per_card': 8,
    'save_dir': None
}

# Emojis to resemble the classic Dobble game
CLASSIC_DOBBLE_EMOJIS = [
    {'mode': 'color', 'group': 'travel-places', 'hex': '2693'},     # anchor
    {'mode': 'color', 'group': 'food-drink', 'hex': '1F37C'},       # baby bottle
    {'mode': 'color', 'group': 'smileys-emotion', 'hex': '1F4A3'},  # bomb
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F335'},   # cactus
    {'mode': 'color', 'group': 'objects', 'hex': '1F56F'},          # candle
    {'mode': 'color', 'group': 'food-drink', 'hex': '1F955'},       # carrot
    {'mode': 'color', 'group': 'food-drink', 'hex': '1F9C0'},       # cheese wedge
    {'mode': 'color', 'group': 'activities', 'hex': '265F'},        # chess pawn
    {'mode': 'color', 'group': 'travel-places', 'hex': '1F3DB'},    # classical building
    {'mode': 'color', 'group': 'smileys-emotion', 'hex': '1F921'},  # clown face
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F333'},   # deciduous tree
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F436'},   # dog face
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F42C'},   # dolphin
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F409'},   # dragon
    {'mode': 'color', 'group': 'travel-places', 'hex': '1F4A7'},    # droplet
    {'mode': 'color', 'group': 'people-body', 'hex': '1F441'},      # eye
    {'mode': 'color', 'group': 'travel-places', 'hex': '1F525'},    # fire
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F340'},   # four leaf clover
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F425'},   # front-facing baby chick
    {'mode': 'color', 'group': 'smileys-emotion', 'hex': '1F47B'},  # ghost
    {'mode': 'color', 'group': 'extras-openmoji', 'hex': 'E1CD'},   # gps
    {'mode': 'color', 'group': 'food-drink', 'hex': '1F34F'},       # green apple
    {'mode': 'color', 'group': 'smileys-emotion', 'hex': '1F638'},  # grinning cat with smiling eyes
    {'mode': 'color', 'group': 'objects', 'hex': '1F528'},          # hammer
    {'mode': 'color', 'group': 'people-body', 'hex': '1F590'},      # hand with fingers splayed
    {'mode': 'color', 'group': 'travel-places', 'hex': '26A1'},     # high voltage
    {'mode': 'color', 'group': 'food-drink', 'hex': '1F9CA'},       # ice
    {'mode': 'color', 'group': 'extras-openmoji', 'hex': 'E24B'},   # intricate
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F41E'},   # lady beetle
    {'mode': 'color', 'group': 'travel-places', 'hex': '1F31C'},    # last quarter moon face
    {'mode': 'color', 'group': 'objects', 'hex': '1F4A1'},          # light bulb
    {'mode': 'color', 'group': 'objects', 'hex': '1F512'},          # locked
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F341'},   # maple leaf
    {'mode': 'color', 'group': 'people-body', 'hex': '1F444'},      # mouth
    {'mode': 'color', 'group': 'objects', 'hex': '1F3BC'},          # musical score
    {'mode': 'color', 'group': 'symbols', 'hex': '26D4'},           # no entry
    {'mode': 'color', 'group': 'objects', 'hex': '1F5DD'},          # old key
    {'mode': 'color', 'group': 'travel-places', 'hex': '1F696'},    # oncoming taxi
    {'mode': 'color', 'group': 'objects', 'hex': '270F'},           # pencil
    {'mode': 'color', 'group': 'people-body', 'hex': '1F9CD'},      # person standing
    {'mode': 'color', 'group': 'symbols', 'hex': '2757'},           # red exclamation mark
    {'mode': 'color', 'group': 'smileys-emotion', 'hex': '2764'},   # red heart
    {'mode': 'color', 'group': 'symbols', 'hex': '2753'},           # red question mark
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F3F5'},   # rosette
    {'mode': 'color', 'group': 'objects', 'hex': '2702'},           # scissors
    {'mode': 'color', 'group': 'smileys-emotion', 'hex': '2620'},   # skull and crossbones
    {'mode': 'color', 'group': 'travel-places', 'hex': '2744'},     # snowflake
    {'mode': 'color', 'group': 'travel-places', 'hex': '26C4'},     # snowman without snow
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F578'},   # spider web
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F577'},   # spider
    {'mode': 'color', 'group': 'travel-places', 'hex': '2600'},     # sun
    {'mode': 'color', 'group': 'objects', 'hex': '1F576'},          # sunglasses
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F996'},   # t-rex
    {'mode': 'color', 'group': 'extras-openmoji', 'hex': 'E0AB'},   # timer
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F422'},   # turtle
    {'mode': 'color', 'group': 'symbols', 'hex': '262F'},           # yin yang
    {'mode': 'color', 'group': 'animals-nature', 'hex': '1F993'}    # zebra
]
