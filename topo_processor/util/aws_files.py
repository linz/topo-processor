import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
from urllib.parse import urlparse

import boto3
from botocore import exceptions as botocore_exceptions
from linz_logger import get_log

from topo_processor.util.aws_credentials import Credentials, get_credentials
from topo_processor.util.configuration import historical_imagery_bucket
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


def create_s3_manifest(manifest_source_path: str) -> None:
    start_time = time_in_ms()
    get_log().debug("check_manifest", manifestPath=manifest_source_path)
    create_manifest_file = False

    url_o = urlparse(manifest_source_path)
    bucket_name = url_o.netloc
    manifest_path = url_o.path[1:]
    credentials: Credentials = get_credentials(bucket_name)

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_session_token=credentials.token,
    )

    try:
        manifest_modified_datetime = s3_client.head_object(Bucket=bucket_name, Key=manifest_path)["LastModified"]
        cutoff_datetime = datetime.now(timezone.utc) - timedelta(days=1)
        if cutoff_datetime > manifest_modified_datetime:
            create_manifest_file = True

    except botocore_exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            get_log().debug("no_manifest_file_found", bucketName=bucket_name, manifestPath=manifest_path, error=e)
            create_manifest_file = True
        else:
            raise e

    try:
        if create_manifest_file:
            get_log().debug("create_manifest", bucketName=bucket_name, manifestPath=manifest_path)
            manifest_new: Dict[str, Any] = {}
            manifest_file_list = _list_objects(historical_imagery_bucket)
            manifest_new["path"] = manifest_path
            manifest_new["time"] = time_in_ms()
            manifest_new["files"] = manifest_file_list
        else:
            return

        s3_client.put_object(
            Body=json.dumps(manifest_new).encode("UTF-8"),
            ContentType="application/json",
            Bucket=bucket_name,
            Key=manifest_path,
        )

    except Exception as e:
        get_log().error("create_manifest_failed", bucketPath=bucket_name, manifestPath=manifest_path, error=e)
        raise e

    get_log().debug(
        "log_manifest_create_time",
        manifestSourcePath=manifest_source_path,
        duration=time_in_ms() - start_time,
    )


def _list_objects(bucket_name: str) -> List[Dict[str, str]]:

    credentials: Credentials = get_credentials(bucket_name)

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_session_token=credentials.token,
    )

    file_list: List[Dict[str, str]] = []
    paginator = s3_client.get_paginator("list_objects_v2")
    response_iterator = paginator.paginate(Bucket=bucket_name)
    for response in response_iterator:
        for contents_data in response["Contents"]:
            key = contents_data["Key"]
            if key.endswith((".tif", ".tiff")):
                file_list.append({"path": key})

    return file_list
