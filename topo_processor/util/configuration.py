from os import environ
from tempfile import mkdtemp
from typing import Optional

from dotenv import load_dotenv

load_dotenv()
lds_cache_bucket: str = environ.get("LDS_CACHE_BUCKET")
aws_role_config_path: str = environ.get("AWS_ROLES_CONFIG")
aws_profile: str = environ.get("AWS_PROFILE")
temp_folder: str = mkdtemp()
