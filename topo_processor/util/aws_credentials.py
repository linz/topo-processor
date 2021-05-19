import os

import boto3

default_credentials = {}
session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
client = session.client("sts")
bucket_roles = {}


def get_credentials(bucket_name: str):

    if bucket_name in bucket_roles:
        if not bucket_roles[bucket_name]["client"]:
            client.assume_role(RoleArn=bucket_roles[bucket_name]["role"])
            bucket_roles[bucket_name]["client"] = client
        cred = bucket_roles[bucket_name]["client"].get("Credentials")
        return {
            "access_key": cred.get("AccessKeyId"),
            "secret_key": cred.get("SecretAccessKey"),
            "token": cred.get("SessionToken"),
        }

    if not default_credentials:
        session_credentials = session.get_credentials()
        default_credentials["access_key"] = session_credentials.access_key
        default_credentials["secret_key"] = session_credentials.secret_key
        default_credentials["token"] = session_credentials.token
    return default_credentials
