import datetime
import os

import boto3
import botocore
from dateutil.tz import tzlocal

default_credentials = {}
session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
client = session.client("sts")
bucket_roles = {}
assume_role_cache: dict = {}


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


def assumed_role_session(role_arn: str, base_session: botocore.session.Session = None) -> boto3.Session:
    base_session = base_session or boto3.session.Session()._session
    fetcher = botocore.credentials.AssumeRoleCredentialFetcher(
        client_creator=base_session.create_client,
        source_credentials=base_session.get_credentials(),
        role_arn=role_arn,
    )
    credentials = botocore.credentials.DeferredRefreshableCredentials(
        method="assume-role", refresh_using=fetcher.fetch_credentials, time_fetcher=lambda: datetime.datetime.now(tzlocal())
    )
    botocore_session = botocore.session.Session()
    botocore_session._credentials = credentials
    return boto3.Session(botocore_session=botocore_session)


def assume_role(bucket_role, sts_client):
    assumed_role_object = sts_client.assume_role(RoleArn=bucket_role, RoleSessionName="AssumeRoleSessionRead")

    credentials = assumed_role_object["Credentials"]

    os.environ["AWS_ACCESS_KEY_ID"] = credentials["AccessKeyId"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = credentials["SecretAccessKey"]
    os.environ["AWS_SESSION_TOKEN"] = credentials["SessionToken"]
