import json

from .get_fs import get_fs


def write_json(dictionary: str, to_json):
    with get_fs(to_json).open(to_json, "w") as f1:
        f1.write(json.dumps(dictionary, indent=4))
