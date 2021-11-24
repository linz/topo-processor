import json
import os
from typing import Dict

import boto3

from topo_processor.util.configuration import aws_roles_config


class Credential:
    access_key: str
    secret_key: str
    token: str

    def __init__(self, access_key: str, secret_key: str, token: str):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token


default_credentials: Credential
session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
client = session.client("sts")
bucket_roles: Dict[str, str] = {}
assume_role_cache: dict = {}


def get_credentials(bucket_name: str) -> Credential:
    if not bucket_roles:
        load_roles(aws_roles_config)

    if bucket_name in bucket_roles:
        if not bucket_roles[bucket_name]["client"]:
            client.assume_role(RoleArn=bucket_roles[bucket_name]["role"])
            bucket_roles[bucket_name]["client"] = client
        cred = bucket_roles[bucket_name]["client"].get("Credentials")
        return Credential(cred.get("AccessKeyId"), cred.get("SecretAccessKey"), cred.get("SessionToken"))

    if not default_credentials:
        session_credentials = session.get_credentials()
        default_credentials = Credential(
            session_credentials.access_key, session_credentials.secret_key, session_credentials.token
        )
    return default_credentials


def load_roles(role_config_path: str) -> None:
    config_file = open(role_config_path)
    config_data = json.load(config_file)

    for element in config_data:
        bucket_roles[element]["role"] = element["roleArn"]
