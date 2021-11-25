import json
import os
from typing import Dict

import boto3

from topo_processor.file_system.get_fs import bucket_name_from_path
from topo_processor.util.configuration import aws_role_config_path


class Credentials:
    access_key: str
    secret_key: str
    token: str

    def __init__(self, access_key: str, secret_key: str, token: str):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token


default_credentials: Credentials
session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
client: boto3.client = session.client("sts")
bucket_roles: Dict[str, str] = {}
assume_role_cache: dict = {}


def get_credentials(bucket_name: str) -> Credentials:
    if not bucket_roles:
        load_roles(json.load(open(aws_role_config_path)))
    if bucket_name in bucket_roles:
        if not "credentials" in bucket_roles[bucket_name]:
            assumed_role_object = client.assume_role(
                RoleArn=bucket_roles[bucket_name]["roleArn"], RoleSessionName="TopoProcessor"
            )
            bucket_roles[bucket_name]["credentials"] = Credentials(
                assumed_role_object["Credentials"]["AccessKeyId"],
                assumed_role_object["Credentials"]["SecretAccessKey"],
                assumed_role_object["Credentials"]["SessionToken"],
            )
        return bucket_roles[bucket_name]["credentials"]

    if not default_credentials:
        session_credentials = session.get_credentials()
        default_credentials = Credentials(
            session_credentials.access_key, session_credentials.secret_key, session_credentials.token
        )
    return default_credentials


def load_roles(role_config: str) -> None:
    for (key, value) in role_config.items():
        bucket_roles[bucket_name_from_path(key)] = value
