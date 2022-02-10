from os import environ
from tempfile import mkdtemp
from typing import cast, Optional

from dotenv import load_dotenv

load_dotenv()
lds_cache_bucket: str = cast(str, environ.get("LDS_CACHE_BUCKET"))
linz_ssm_bucket_config_name = environ.get("LINZ_SSM_BUCKET_CONFIG_NAME")
aws_profile: str = cast(str, environ.get("AWS_PROFILE"))
temp_folder: str = mkdtemp()
