import gzip
import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.util.gzip import is_gzip_file


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


def test_is_gzip_file_true(setup):
    compressed_file = os.path.abspath(os.path.join(setup, "file.gz"))
    cf = gzip.open(compressed_file, "wb")
    cf.write("test".encode("utf-8"))
    cf.close()

    assert is_gzip_file(compressed_file) == True


def test_is_gzip_file_false(setup):
    file = os.path.abspath(os.path.join(setup, "file.txt"))
    cf = open(file, "wb")
    cf.write("test".encode("utf-8"))
    cf.close()

    assert is_gzip_file(file) == False
