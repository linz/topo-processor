import pytest
from fsspec.implementations.local import LocalFileSystem
from s3fs.core import S3FileSystem

from topo_processor.file_system.get_fs import get_fs


@pytest.mark.skip(reason="Skip this test for now before refactoring get_credentials")
def test_get_fs_s3() -> None:
    path = "s3://testbucket"
    assert isinstance(get_fs(path), S3FileSystem)


def test_get_fs_local() -> None:
    path = "./test"
    assert isinstance(get_fs(path), LocalFileSystem)
    path = "/home/test/location"
    assert isinstance(get_fs(path), LocalFileSystem)
