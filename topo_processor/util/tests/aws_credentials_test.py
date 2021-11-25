import json

import pytest

from topo_processor.util.aws_credentials import bucket_roles, load_roles


def test_load_roles():
    role_config = json.loads('{"s3://example-bucket": {"roleArn": "arn:aws:iam::0123456789:role/example-read"}}')
    load_roles(role_config)
    assert bucket_roles["example-bucket"]["roleArn"] == "arn:aws:iam::0123456789:role/example-read"


@pytest.mark.skip(reason="Need to mock AWS to implement this test")
def test_get_credentials():
    # TODO: Mock AWS
    pass
