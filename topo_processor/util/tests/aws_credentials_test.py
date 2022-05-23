import pytest

from topo_processor.util.aws_credentials import bucket_roles, get_role_arn


# Add test with AWS mock
def test_get_role_arn() -> None:
    bucket_roles["bucket-test"] = {"roleArn": "arn:aws:iam::123456789012:role/S3Access"}
    assert get_role_arn("bucket-test") == "arn:aws:iam::123456789012:role/S3Access"
