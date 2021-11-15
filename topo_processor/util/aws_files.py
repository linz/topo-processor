import json
from urllib.parse import urlparse

import boto3
from linz_logger import get_log

from topo_processor.util.aws_credentials import assumed_role_session


def s3_download(source_path: str, dest_path: str, role_arn: str):
    get_log().debug("s3_download", objectPath=source_path, destinationPath=dest_path, roleArn=role_arn)
    url_o = urlparse(source_path)
    bucket_name = url_o.netloc
    object_name = url_o.path[1:]

    session = assumed_role_session(role_arn)
    s3 = session.resource("s3")
    try:
        s3.Bucket(bucket_name).download_file(object_name, dest_path)
    except Exception as e:
        get_log().error(f"An error has occurred while downloading {source_path}: {e}")
        raise e


def load_file_content(bucket_name: str, object_path: str, role_arn: str):
    session: boto3.Session = assumed_role_session(role_arn)
    s3 = session.client("s3")
    object_content = s3.get_object(Bucket=bucket_name, Key=object_path)

    if object_path.endswith(".json"):
        return json.loads(object_content["Body"].read().decode("utf-8"))

    return object_content["Body"].read().decode("utf-8")


def build_s3_path(bucket_name: str, object_path: str) -> str:
    return "s3://" + bucket_name + "/" + (object_path[1:] if object_path.startswith("/") else object_path)
