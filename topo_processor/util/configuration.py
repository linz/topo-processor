from os import environ
from tempfile import mkdtemp
from typing import Optional, cast

from dotenv import load_dotenv

load_dotenv()


lds_cache_bucket: str = cast(str, environ.get("LDS_CACHE_BUCKET"))
if not lds_cache_bucket:
    raise Exception("$LDS_CACHE_BUCKET is not set")
linz_ssm_bucket_config_name = environ.get("LINZ_SSM_BUCKET_CONFIG_NAME")
aws_profile: Optional[str] = environ.get("AWS_PROFILE")
temp_folder: str = mkdtemp()
