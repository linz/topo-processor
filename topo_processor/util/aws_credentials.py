import json
import os
from typing import TYPE_CHECKING, Any, Dict

from boto3 import Session

from topo_processor.file_system.get_fs import bucket_name_from_path
from topo_processor.util.configuration import aws_role_config_path

if TYPE_CHECKING:
    from mypy_boto3_sts import STSClient
else:
    STSClient = object


class Credentials:
    access_key: str
    secret_key: str
    token: str

    def __init__(self, access_key: str, secret_key: str, token: str):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token


session = Session(profile_name=os.getenv("AWS_PROFILE"))
client_sts: STSClient = session.client("sts")
bucket_roles: Dict = {}


def get_credentials(bucket_name: str) -> Credentials:
    if not bucket_roles:
        load_roles(json.load(open(aws_role_config_path)))
    if bucket_name in bucket_roles:
        if not "credentials" in bucket_roles[bucket_name]:
            assumed_role_object = client_sts.assume_role(  #
                RoleArn=bucket_roles[bucket_name]["roleArn"], RoleSessionName="TopoProcessor"
            )
            bucket_roles[bucket_name]["credentials"] = Credentials(
                assumed_role_object["Credentials"]["AccessKeyId"],
                assumed_role_object["Credentials"]["SecretAccessKey"],
                assumed_role_object["Credentials"]["SessionToken"],
            )
        return bucket_roles[bucket_name]["credentials"]

    session_credentials = session.get_credentials()
    default_credentials = Credentials(
        session_credentials.access_key, session_credentials.secret_key, session_credentials.token
    )

    return default_credentials


def load_roles(role_config: Any) -> None:
    for (key, value) in role_config.items():
        bucket_roles[bucket_name_from_path(key)] = value
