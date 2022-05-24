import json
from typing import Any, Dict

import boto3
from linz_logger import get_log

ROLE_ARN_PROD = "arn:aws:iam::715898075157:role/api-users"
ROLE_ARN_NONPROD = "arn:aws:iam::632223577832:role/nonprod-api-users"


def invoke_lambda(name: str, http_method: str, parameters: Dict[str, str]) -> Dict[str, Any]:
    client_lambda = boto3.client("lambda")
    client_sts = boto3.client("sts")

    # TODO Change that before commit
    name = "nonprod-" + name
    role_arn = ROLE_ARN_NONPROD

    client_sts.assume_role(RoleArn=role_arn, RoleSessionName="read-session")
    payload = build_lambda_payload(http_method, parameters)
    get_log().debug("invoke_lambda_function", name=name, payload=payload)

    raw_response = client_lambda.invoke(
        FunctionName=name,
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=json.dumps(payload).encode(),
    )
    payload_response: Dict[str, Any] = json.loads(raw_response["Payload"].read())

    if not is_response_ok(payload_response):
        raise Exception("invoke_lambda_function_error", payload_response)

    get_log().debug("response_lambda_function", name=name, response=payload_response)
    return payload_response


def build_lambda_payload(http_method: str, parameters: Dict[str, str]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    payload["http_method"] = http_method
    payload["body"] = {}
    if parameters:
        payload["body"] = parameters

    return payload


def invoke_import_status(execution_arn: str) -> Dict[str, Any]:
    """Return the current status of the dataset version import process in the Geostore identified by 'execution_arn'"""
    import_status_parameters = {"execution_arn": execution_arn}
    import_status_response_payload = invoke_lambda("import-status", "GET", import_status_parameters)

    import_status: Dict[str, Any] = import_status_response_payload["body"]
    return import_status


def is_response_ok(response: Dict[str, Any]) -> bool:
    try:
        if 200 <= response["status_code"] <= 299:
            return True
        return False
    except Exception as e:
        raise Exception("There is an issue with the response") from e
