import pytest

from topo_processor.geostore.invoke import build_lambda_payload


def test_build_lambda_payload() -> None:
    payload = {
        "http_method": "GET",
        "body": {"id": "123", "metadata_url": "s3://my-bucket/my-survey/metadata.csv", "s3_role_arn": "arn:my-arn:1234567"},
    }
    payload_param = {
        "id": "123",
        "metadata_url": "s3://my-bucket/my-survey/metadata.csv",
        "s3_role_arn": "arn:my-arn:1234567",
    }

    payload_built = build_lambda_payload("GET", payload_param)
    assert payload == payload_built
