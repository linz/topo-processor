from .file_system_local import FileSystemLocal
from .file_system_s3 import FileSystemS3


def get_file_system(target: str):
    if target.startswith("s3://"):
        return FileSystemS3()
    return FileSystemLocal()
