
CHARACTER_MAP = {
    "fa": {
        "arrows-alt": {
            "char": "f0b2",
            "size": 18,
            "x": -8,
            "y": 7,
        },
        "clock-o": {
            "char": "f017",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "clone": {
            "char": "f24d",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "cube": {
            "char": "f1b2",
            "size": 18,
            "x": -8,
            "y": 6,
        },
        "cubes": {
            "char": "f1b3",
            "size": 18,
            "x": -11,
            "y": 6,
        },
        "file-text-o": {
            "char": "f0f6",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "hdd-o": {
            "char": "f0a0",
            "size": 20,
            "x": -9,
            "y": 7,
        },
        "key": {
            "char": "f084",
            "size": 18,
            "x": -9,
            "y": 5,
        },
        "lock": {
            "char": "f023",
            "size": 18,
            "x": -7,
            "y": 7,
        },
        "map-signs": {
            "char": "f277",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "object-group": {
            "char": "f247",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "podcast": {
            "char": "f2ce",
            "size": 18,
            "x": -8.5,
            "y": 7,
        },
        "server": {
            "char": "f233",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "share-alt": {
            "char": "f1e0",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "tasks": {
            "char": "f0ae",
            "size": 18,
            "x": -9,
            "y": 7,
        },
        "user": {
            "char": "f007",
            "size": 18,
            "x": -7,
            "y": 7,
        }
    }
}

FAMILY_MAP = {
    "fa": "FontAwesome",
}


def get_icon(icon):
    family, character = icon.split(":")
    output = CHARACTER_MAP[family][character].copy()
    output["family"] = FAMILY_MAP[family]
    output['name'] = character
    output["char"] = int("0x{}".format(output["char"]), 0)
    return output
