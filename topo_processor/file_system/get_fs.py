from fsspec.implementations.local import LocalFileSystem
from s3fs import S3FileSystem


def is_s3_path(path: str) -> bool:
    if path.startswith("s3://"):
        return True
    return False


def bucket_name_from_path(path: str) -> str:
    path_parts = path.replace("s3://", "").split("/")
    return path_parts.pop(0)


def get_fs(path: str):
    if is_s3_path(path):
        return S3FileSystem()
    return LocalFileSystem(auto_mkdir="True")
