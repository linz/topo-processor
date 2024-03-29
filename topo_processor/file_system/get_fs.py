from typing import Any

from fsspec.implementations.local import LocalFileSystem
from s3fs import S3FileSystem

from topo_processor.util.aws_credentials import Credentials, get_credentials_from_bucket
from topo_processor.util.s3 import bucket_name_from_path, is_s3_path


def get_fs(path: str) -> Any:
    if is_s3_path(path):
        credentials: Credentials = get_credentials_from_bucket(bucket_name_from_path(path))
        return S3FileSystem(secret=credentials.secret_key, token=credentials.token, key=credentials.access_key)
    return LocalFileSystem(auto_mkdir="True")
