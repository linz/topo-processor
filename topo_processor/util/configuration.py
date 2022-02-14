from os import environ
from tempfile import mkdtemp
from typing import Optional, cast

from dotenv import load_dotenv

load_dotenv()
lds_cache_bucket: Optional[str] = environ.get("LDS_CACHE_BUCKET")
if lds_cache_bucket is None:
    raise Exception("$LDS_CACHE_BUCKET is not set")
linz_ssm_bucket_config_name = environ.get("LINZ_SSM_BUCKET_CONFIG_NAME")
aws_profile: Optional[str] = environ.get("AWS_PROFILE")
if aws_profile is None:
    raise Exception("$AWS_PROFILE is not set")
temp_folder: str = mkdtemp()
