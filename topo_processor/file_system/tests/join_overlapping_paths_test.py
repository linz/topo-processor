from topo_processor.file_system.join_overlapping_paths import join_overlapping_paths


def test_join_overlapping_paths_aws():
    p1 = "s3://bucketname/folder"
    p2 = "/bucketname/folder/subfolder/file.txt"
    full_path = join_overlapping_paths(p1, p2)
    assert full_path == "s3://bucketname/folder/subfolder/file.txt"


def test_join_overlapping_paths_local():
    p1 = "/home/username/dev/topo-processor/test_data/tiffs"
    p2 = "/test_data/tiffs/SURVEY_1/CONTROL.tiff"
    full_path = join_overlapping_paths(p1, p2)
    assert full_path == "/home/username/dev/topo-processor/test_data/tiffs/SURVEY_1/CONTROL.tiff"


def test_join_overlapping_paths_inverse_input_paths():
    p1 = "/home/username/dev/topo-processor/test_data/tiffs"
    p2 = "/test_data/tiffs/SURVEY_1/CONTROL.tiff"
    full_path = join_overlapping_paths(p2, p1)
    assert full_path == "/home/username/dev/topo-processor/test_data/tiffs/SURVEY_1/CONTROL.tiff"
