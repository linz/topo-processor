def bucket_name_from_path(path: str) -> str:
    path_parts = path.replace("s3://", "").split("/")
    return path_parts.pop(0)


def is_s3_path(path: str) -> bool:
    if path.startswith("s3://"):
        return True
    return False
