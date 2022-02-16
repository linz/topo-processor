from os import environ
from tempfile import mkdtemp
from typing import Optional

from dotenv import load_dotenv
from linz_logger import get_log

load_dotenv()


def get_env(env_name: str) -> str:
    env_var = environ.get(env_name)
    if env_var is None:
        raise Exception(f"Missing environment variable ${env_name}")
    return env_var


lds_cache_bucket: str = get_env("LINZ_CACHE_BUCKET")
aws_profile: Optional[str] = environ.get("AWS_PROFILE")
linz_ssm_bucket_config_name: Optional[str] = environ.get("LINZ_SSM_BUCKET_CONFIG_NAME")
temp_folder: str = mkdtemp()
get_log().debug(
    "from_environment_variables", lds_cache_bucket=lds_cache_bucket, aws_profile=aws_profile, ssm=linz_ssm_bucket_config_name
)
