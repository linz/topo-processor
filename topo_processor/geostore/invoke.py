import json
from typing import TYPE_CHECKING, Any, Dict

from linz_logger import get_log

if TYPE_CHECKING:
    from mypy_boto3_lambda import Client
else:
    Client = object


def invoke_lambda(client: Client, name: str, http_method: str, parameters: Dict[str, str]) -> Dict[str, Any]:
    payload = b'{"http_method": "' + http_method.encode() + b'", "body": {'
    if len(parameters.items()) > 0:
        for key, value in parameters.items():
            payload = payload + b'"' + key.encode() + b'": "' + value.encode() + b'",'
        payload = payload[:-1]
    payload = payload + b"}}"
    get_log().debug("invoke_lambda_function", name=name, payload=payload)

    raw_response = client.invoke(
        FunctionName=name,
        InvocationType="RequestResponse",
        LogType="Tail",
        Payload=payload,
    )
    payload_response: Dict[str, Any] = json.loads(raw_response["Payload"].read())

    get_log().debug("response_lambda_function", name=name, response=payload_response)
    return payload_response


def invoke_import_status(client: Client, environment: str, execution_arn: str) -> Dict[str, Any]:
    """Return the current status of the dataset version import process in the Geostore identified by 'execution_arn'"""
    import_status_parameters = {"execution_arn": execution_arn}
    import_status_response_payload = invoke_lambda(client, f"{environment}-import-status", "GET", import_status_parameters)
    if "status_code" not in import_status_response_payload or import_status_response_payload["status_code"] != 200:
        raise Exception("Error while retrieving the import status from the Geostore", import_status_response_payload)

    import_status: Dict[str, Any] = import_status_response_payload["body"]
    return import_status
