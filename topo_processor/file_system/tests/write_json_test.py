import os

import pytest

from topo_processor.file_system.write_json import write_json


def test_write_json(setup: str) -> None:
    my_dict = {"foo": "foo", "bar": 1}
    target = setup + "/test.json"
    write_json(my_dict, target)
    assert os.path.isfile(target)
