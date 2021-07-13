from fsspec.implementations.local import LocalFileSystem
from s3fs import S3FileSystem

from topo_processor.file_system.get_path_with_protocol import get_path_with_protocol


def test_get_path_with_protocol_aws():
    source_dir_with_forwardslash = "s3://bucketname/folder/"
    path = "bucketname/folder/subfolder/subfolder2"
    fs = S3FileSystem()
    full_path = get_path_with_protocol(source_dir=source_dir_with_forwardslash, source_fs=fs, path=path)
    assert full_path == "s3://bucketname/folder/subfolder/subfolder2"
    source_dir_without_forwardslash = "s3://bucketname/folder"
    full_path = get_path_with_protocol(source_dir=source_dir_without_forwardslash, source_fs=fs, path=path)
    assert full_path == "s3://bucketname/folder/subfolder/subfolder2"


def test_get_path_with_protocol_local():
    source_dir_with_forwardslash = "/home/username/dev/topo-processor/test_data/tiffs/"
    path = "/home/username/dev/topo-processor/test_data/tiffs/SURVEY_1"
    fs = LocalFileSystem(auto_mkdir="True")
    full_path = get_path_with_protocol(source_dir=source_dir_with_forwardslash, source_fs=fs, path=path)
    print(full_path)
    assert full_path == "/home/username/dev/topo-processor/test_data/tiffs/SURVEY_1"
    source_dir_without_forwardslash = "/home/username/dev/topo-processor/test_data/tiffs"
    full_path = get_path_with_protocol(source_dir=source_dir_without_forwardslash, source_fs=fs, path=path)
    print(full_path)
    assert full_path == "/home/username/dev/topo-processor/test_data/tiffs/SURVEY_1"
