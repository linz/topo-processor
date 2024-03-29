from s3fs import S3FileSystem


def get_path_with_protocol(source_dir: str, source_fs: S3FileSystem, path: str) -> str:
    source_dir = source_dir.rstrip("/")
    trimmed_source_dir = source_fs._strip_protocol(source_dir)
    output_path = f"{source_dir}{path[(len(trimmed_source_dir)):]}"
    return output_path
