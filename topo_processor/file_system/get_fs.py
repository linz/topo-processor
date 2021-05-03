import fsspec


def get_fs(path: str):
    if path.startswith("s3://"):
        return fsspec.filesystem("s3")
    return fsspec.filesystem("file", auto_mkdir="True")
