import os

import boto3

credentials = None


def get_credentials():
    global credentials
    if not credentials:
        session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
        credentials = session.get_credentials()
    return credentials
