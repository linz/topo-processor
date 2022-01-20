from os import environ
from tempfile import mkdtemp
from typing import cast

from dotenv import load_dotenv

load_dotenv()
lds_cache_bucket: str = cast(str, environ.get("LDS_CACHE_BUCKET"))
aws_role_config_path: str = environ.get("AWS_ROLES_CONFIG")
aws_profile: str = cast(str, environ.get("AWS_PROFILE"))
temp_folder: str = mkdtemp()
