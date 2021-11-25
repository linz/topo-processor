import json
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


def load_file_content(bucket_name: str, object_path: str) -> None:
    credentials: Credentials = get_credentials(bucket_name)

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_session_token=credentials.token,
    )

    object_content = s3.Object(bucket_name=bucket_name, key=object_path)

    if object_path.endswith(".json"):
        return json.loads(object_content.get()["Body"].read())

    return object_content.get()["Body"].read()


def build_s3_path(bucket_name: str, object_path: str) -> str:
    return "s3://" + bucket_name + "/" + (object_path[1:] if object_path.startswith("/") else object_path)
