import json
from typing import TYPE_CHECKING, Any, Dict

from linz_logger import get_log

from topo_processor.geostore.environment import is_production

if TYPE_CHECKING:
    from mypy_boto3_lambda import Client
else:
    Client = object


def invoke_lambda(client: Client, name: str, http_method: str, parameters: Dict[str, str]) -> Dict[str, Any]:
    if not is_production():
        name = "nonprod-" + name
    payload = build_lambda_payload(http_method, parameters)
    get_log().debug("invoke_lambda_function", name=name, payload=payload)

    raw_response = client.invoke(
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


def invoke_import_status(client: Client, execution_arn: str) -> Dict[str, Any]:
    """Return the current status of the dataset version import process in the Geostore identified by 'execution_arn'"""
    import_status_parameters = {"execution_arn": execution_arn}
    import_status_response_payload = invoke_lambda(client, "import-status", "GET", import_status_parameters)

    import_status: Dict[str, Any] = import_status_response_payload["body"]
    return import_status


def is_response_ok(response: Dict[str, Any]) -> bool:
    try:
        if 200 <= response["status_code"] <= 299:
            return True
        return False
    except Exception as e:
        raise Exception("There is an issue with the response") from e
