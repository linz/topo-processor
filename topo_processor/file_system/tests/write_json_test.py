import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.file_system.write_json import write_json


@pytest.fixture(autouse=True)
def setup():
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    target = mkdtemp()
    yield target
    shutil.rmtree(target)


def test_write_json(setup):
    my_dict = {"foo": "foo", "bar": 1}
    target = setup + "/test.json"
    write_json(my_dict, target)
    assert os.path.isfile(target)
