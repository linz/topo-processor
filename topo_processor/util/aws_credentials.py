import json
from typing import TYPE_CHECKING, Any, Dict

from boto3 import Session

from topo_processor.util.configuration import aws_profile, linz_ssm_bucket_config_name
from topo_processor.util.s3 import bucket_name_from_path

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


session = Session(profile_name=aws_profile)
client_sts: STSClient = session.client("sts")
bucket_roles: Dict[str, Dict[str, str]] = {}
bucket_credentials: Dict[str, Credentials] = {}

# Load bucket to roleArn mapping for LINZ internal buckets from SSM
def init_roles() -> None:
    if linz_ssm_bucket_config_name is None:
        return
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> refactor: move ssm loading inside init_roles to prevent unit test failures

    if aws_profile is None:
        return

    role_config_param = session.client("ssm").get_parameter(Name=linz_ssm_bucket_config_name)
<<<<<<< HEAD
=======
    role_config_param = client_ssm.get_parameter(Name=linz_ssm_bucket_config_name)
>>>>>>> feat: import bucket role arns from ssm
=======
>>>>>>> refactor: move ssm loading inside init_roles to prevent unit test failures
    role_config = json.loads(role_config_param["Parameter"]["Value"])

    for cfg in role_config:
        bucket_roles[cfg["bucket"]] = cfg


def get_credentials(bucket_name: str) -> Credentials:
    if not bucket_roles:
        init_roles()
    if bucket_name in bucket_roles:
        # FIXME: check if the token is expired - add a parameter
        if bucket_name not in bucket_credentials:
            assumed_role_object = client_sts.assume_role(
                RoleArn=bucket_roles[bucket_name]["roleArn"], RoleSessionName="TopoProcessor"
            )
            bucket_credentials[bucket_name] = Credentials(
                assumed_role_object["Credentials"]["AccessKeyId"],
                assumed_role_object["Credentials"]["SecretAccessKey"],
                assumed_role_object["Credentials"]["SessionToken"],
            )
        return bucket_credentials[bucket_name]

    session_credentials = session.get_credentials()
    default_credentials = Credentials(
        session_credentials.access_key, session_credentials.secret_key, session_credentials.token
    )

    return default_credentials
