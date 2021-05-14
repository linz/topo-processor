import os

import boto3

credentials = None
role_dict = {}


def get_credentials(bucket_name: str):
    global credentials
    if credentials:
        return credentials

    session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))

    if bucket_name in role_dict:
        if not role_dict[bucket_name]["client"]:
            client = boto3.client()
            client.assume_role(RoleArn=role_dict[bucket_name]["role"])
            role_dict[bucket_name]["client"] = client
        cred = role_dict[bucket_name]["client"].get("Credentials")
        credentials = {
            "access_key": cred.get("AccessKeyId"),
            "secret_key": cred.get("SecretAccessKey"),
            "token": cred.get("SessionToken"),
        }
    else:
        session_credentials = session.get_credentials()
        credentials = {
            "access_key": session_credentials.access_key,
            "secret_key": session_credentials.secret_key,
            "token": session_credentials.token,
        }
    return credentials
