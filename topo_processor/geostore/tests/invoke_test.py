import pytest

from topo_processor.geostore.invoke import build_lambda_payload, is_response_ok


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


def test_is_response_ok() -> None:
    response_ko = {"status_code": 404, "body": {"message": "Not Found: dataset '1234' does not exist"}}
    assert is_response_ok(response_ko) is False
    response_ok = {
        "status_code": 200,
        "body": {
            "created_at": "2022-03-23T02:41:53.940795+0000",
            "pk": "DATASET#01FYTADW8MSCNR8D68EX7APMD3",
            "title": "test_title",
            "updated_at": "2022-03-23T02:41:53.940911+0000",
            "id": "01FYTADW8MSCNR8D68EX7APMD3",
        },
    }
    assert is_response_ok(response_ok)
