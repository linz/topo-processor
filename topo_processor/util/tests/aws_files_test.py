import shutil
from tempfile import mkdtemp
from typing import Generator

import pytest

from topo_processor.util.aws_files import build_s3_path


@pytest.fixture(autouse=True)
def setup() -> Generator[str, None, None]:
    """
    This function creates a temporary directory and deletes it after each test.
    See following link for details:
    https://docs.pytest.org/en/stable/fixture.html#yield-fixtures-recommended
    """
    target = mkdtemp()
    yield target
    shutil.rmtree(target)


# Add test with AWS mock


def test_build_s3_path() -> None:
    assert build_s3_path("test-bucket", "/test-folder/object.ext") == "s3://test-bucket/test-folder/object.ext"
