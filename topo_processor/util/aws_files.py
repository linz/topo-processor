import json
from datetime import datetime, timezone
from typing import Any, Dict
from urllib.parse import urlparse

import boto3
from linz_logger import get_log

from topo_processor.util.aws_credentials import Credentials, get_credentials
from topo_processor.util.time import time_in_ms


def s3_download(source_path: str, dest_path: str) -> None:
    start_time = time_in_ms()
    get_log().debug("s3_download started", objectPath=source_path, destinationPath=dest_path)
    url_o = urlparse(source_path)
    bucket_name = url_o.netloc
    object_name = url_o.path[1:]
    credentials: Credentials = get_credentials(bucket_name)

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_session_token=credentials.token,
    )

    try:
        s3.Bucket(bucket_name).download_file(object_name, dest_path)
    except Exception as e:
        get_log().error("s3_download failed", objectPath=source_path, error=e)
        raise e

    get_log().debug(
        "s3_download ended",
        objectPath=source_path,
        destinationPath=dest_path,
        duration=time_in_ms() - start_time,
    )


def load_file_content(bucket_name: str, object_path: str) -> Dict[str, Any]:
    get_log().debug("bucket_name", bucket_name=bucket_name)
    credentials: Credentials = get_credentials(bucket_name)

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_session_token=credentials.token,
    )

    object_content = s3.Object(bucket_name=bucket_name, key=object_path)

    if object_path.endswith(".json"):
        json_result: Dict[str, Any] = json.loads(object_content.get()["Body"].read())
        return json_result

    result: Dict[str, Any] = json.loads(object_content.get()["Body"].read().decode("utf-8"))
    return result


def build_s3_path(bucket_name: str, object_path: str) -> str:
    return f"s3://{bucket_name}/" + (object_path[1:] if object_path.startswith("/") else object_path)


def bucket_name_from_path(path: str) -> str:
    path_parts = path.replace("s3://", "").split("/")
    return path_parts.pop(0)


def is_s3_path(path: str) -> bool:
    if path.startswith("s3://"):
        return True
    return False

def build_s3_manifest(source_path: str) -> datetime:
    start_time = time_in_ms()
    get_log().debug("s3 timestamp", objectPath=source_path)

    url_o = urlparse(source_path)
    bucket_name = url_o.netloc
    object_name = url_o.path[1:]
    credentials: Credentials = get_credentials(bucket_name)

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_session_token=credentials.token,
    )

    try:
        object_summary = s3.ObjectSummary(bucket_name,object_name)
        print(object_summary)
    except Exception as e:
        get_log().error("s3_download failed", objectPath=source_path, error=e)
        raise e

    get_log().debug(
        "log_manifest_details",
        objectPath=source_path,
        duration=time_in_ms() - start_time,
    )
