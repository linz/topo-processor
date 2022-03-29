import json
from typing import TYPE_CHECKING, Any, Dict

from linz_logger import get_log

if TYPE_CHECKING:
    from mypy_boto3_lambda import Client
else:
    Client = object


def invoke_lambda(client: Client, name: str, http_method: str, parameters: Dict[str, str]) -> Dict[str, Any]:
    payload = build_lambda_payload(http_method, parameters)
    get_log().debug("invoke_lambda_function", name=name, payload=payload)

    raw_response = client.invoke(
        FunctionName=name,
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=json.dumps(payload).encode(),
    )
    payload_response: Dict[str, Any] = json.loads(raw_response["Payload"].read())

    get_log().debug("response_lambda_function", name=name, response=payload_response)
    return payload_response


def build_lambda_payload(http_method: str, parameters: Dict[str, str]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    payload["http_method"] = http_method
    payload["body"] = {}
    if parameters:
        payload["body"] = parameters

    return payload


def invoke_import_status(client: Client, environment: str, execution_arn: str) -> Dict[str, Any]:
    """Return the current status of the dataset version import process in the Geostore identified by 'execution_arn'"""
    import_status_parameters = {"execution_arn": execution_arn}
    import_status_response_payload = invoke_lambda(client, f"{environment}-import-status", "GET", import_status_parameters)
    if "status_code" not in import_status_response_payload or import_status_response_payload["status_code"] != 200:
        raise Exception("Error while retrieving the import status from the Geostore", import_status_response_payload)

    import_status: Dict[str, Any] = import_status_response_payload["body"]
    return import_status
