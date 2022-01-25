import gzip
import os

import pytest

from topo_processor.util.gzip import is_gzip_file


def test_is_gzip_file_true(setup: str) -> None:
    compressed_file = os.path.abspath(os.path.join(setup, "file.gz"))
    cf = gzip.open(compressed_file, "wb")
    cf.write("test".encode("utf-8"))
    cf.close()

    assert is_gzip_file(compressed_file) == True


def test_is_gzip_file_false(setup: str) -> None:
    file = os.path.abspath(os.path.join(setup, "file.txt"))
    cf = open(file, "wb")
    cf.write("test".encode("utf-8"))
    cf.close()

    assert is_gzip_file(file) == False
