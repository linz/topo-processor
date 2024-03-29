import json
from typing import TYPE_CHECKING, Dict

from boto3 import Session
from linz_logger import get_log

from topo_processor.util.configuration import aws_profile, linz_ssm_bucket_config_name

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
    get_log().debug("init_roles", linz_ssm_bucket_name=linz_ssm_bucket_config_name, aws_profile=aws_profile)
    if linz_ssm_bucket_config_name is None:
        return

    get_log().debug("load_bucket_config", ssm=linz_ssm_bucket_config_name)
    role_config_param = session.client("ssm").get_parameter(Name=linz_ssm_bucket_config_name)
    role_config = json.loads(role_config_param["Parameter"]["Value"])

    for cfg in role_config:
        bucket_roles[cfg["bucket"]] = cfg
    get_log().info("load_bucket_config_done", ssm=linz_ssm_bucket_config_name, buckets=len(role_config))


def get_credentials_from_bucket(bucket_name: str) -> Credentials:
    get_log().debug("get_credentials_from_bucket", bucket_name=bucket_name)
    # FIXME: check if the token is expired - add a parameter
    if bucket_name not in bucket_credentials:
        role_arn = get_role_arn(bucket_name)
        if role_arn:
            bucket_credentials[bucket_name] = get_credentials_from_role(role_arn)
        else:
            session_credentials = session.get_credentials()
            default_credentials = Credentials(
                session_credentials.access_key, session_credentials.secret_key, session_credentials.token
            )

            return default_credentials
    return bucket_credentials[bucket_name]


def get_credentials_from_role(role_arn: str) -> Credentials:
    get_log().debug("get_credentials_from_role", role_arn=role_arn)
    assumed_role = client_sts.assume_role(RoleArn=role_arn, RoleSessionName="TopoProcessor")
    credentials = Credentials(
        assumed_role["Credentials"]["AccessKeyId"],
        assumed_role["Credentials"]["SecretAccessKey"],
        assumed_role["Credentials"]["SessionToken"],
    )
    return credentials


def get_role_arn(bucket_name: str) -> str:
    role_arn = ""
    if not bucket_roles:
        init_roles()
    if bucket_name in bucket_roles:
        role_arn = bucket_roles[bucket_name]["roleArn"]
    else:
        get_log().warn("role_arn_not_found", bucketName=bucket_name)

    return role_arn
