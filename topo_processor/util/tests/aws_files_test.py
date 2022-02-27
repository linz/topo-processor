import pytest

from topo_processor.aws.aws_files import build_s3_path


# Add test with AWS mock
def test_build_s3_path() -> None:
    assert build_s3_path("test-bucket", "/test-folder/object.ext") == "s3://test-bucket/test-folder/object.ext"
