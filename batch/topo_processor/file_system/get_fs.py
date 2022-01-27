from typing import Any

from fsspec.implementations.local import LocalFileSystem
from s3fs import S3FileSystem


def is_s3_path(path: str) -> bool:
    if path.startswith("s3://"):
        return True
    return False


def get_fs(path: str) -> Any:
    if is_s3_path(path):
        return S3FileSystem()
    return LocalFileSystem(auto_mkdir="True")
