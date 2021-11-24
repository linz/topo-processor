import os
from typing import Dict

import boto3

from topo_processor.file_system.get_fs import bucket_name_from_path
from topo_processor.util.configuration import aws_roles_config


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
client = session.client("sts")
bucket_roles = {}


def get_credentials(bucket_name: str) -> Credentials:
    if not bucket_roles:
        load_roles(aws_roles_config)

    if bucket_name in bucket_roles:
        if not bucket_roles[bucket_name]["client"]:
            client.assume_role(RoleArn=bucket_roles[bucket_name]["role"])
            bucket_roles[bucket_name]["client"] = client
        cred = bucket_roles[bucket_name]["client"].get("Credentials")

        return Credentials(cred.get("AccessKeyId"), cred.get("SecretAccessKey"), cred.get("SessionToken"))

    if not default_credentials:
        session_credentials = session.get_credentials()
        default_credentials = Credentials(
            session_credentials.access_key, session_credentials.secret_key, session_credentials.token
        )

    return default_credentials


def load_roles(roles_config: Dict) -> None:
    for (key, value) in roles_config.items():
        bucket_roles[bucket_name_from_path(key)] = {"role": value["roleArn"]}
