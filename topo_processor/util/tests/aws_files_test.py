import os
import shutil
from tempfile import mkdtemp

import pytest

from topo_processor.util.aws_files import build_s3_path, load_file_content, s3_download


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


# Add test with AWS mock


def test_build_s3_path():
    assert build_s3_path("test-bucket", "/test-folder/object.ext") == "s3://test-bucket/test-folder/object.ext"
