from typing import Any

from fsspec.implementations.local import LocalFileSystem
from s3fs import S3FileSystem

from topo_processor.file_system.s3 import bucket_name_from_path


def is_s3_path(path: str) -> bool:
    if path.startswith("s3://"):
        return True
    return False


def get_fs(path: str) -> Any:
    # FIXME: Find a solution to fix this circular import and move that import
    from topo_processor.util.aws_credentials import Credentials, get_credentials

    if is_s3_path(path):
        credentials: Credentials = get_credentials(bucket_name_from_path(path))
        return S3FileSystem(secret=credentials.secret_key, token=credentials.token, key=credentials.access_key)
    return LocalFileSystem(auto_mkdir="True")
