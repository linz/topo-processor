from os import environ
from tempfile import mkdtemp
from typing import cast

from dotenv import load_dotenv

load_dotenv()


def get_env(env_name: str) -> str:
    env_var = environ.get(env_name)
    if env_var is None:
        raise Exception(f"Missing environment variable ${env_name}")
    return env_var


lds_cache_bucket: str = get_env("LINZ_CACHE_BUCKET")
aws_profile: str = get_env("AWS_PROFILE")
linz_ssm_bucket_config_name = environ.get("LINZ_SSM_BUCKET_CONFIG_NAME")
temp_folder: str = mkdtemp()
