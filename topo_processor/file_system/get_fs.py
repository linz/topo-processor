from fsspec.implementations.local import LocalFileSystem
from s3fs import S3FileSystem


def get_fs(path: str):
    if path.startswith("s3://"):
        return S3FileSystem()
    return LocalFileSystem(auto_mkdir="True")
