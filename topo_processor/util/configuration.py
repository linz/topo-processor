from tempfile import mkdtemp
from typing import Dict

from dotenv import dotenv_values

configuration = dotenv_values(".env")

lds_cache_bucket: str = configuration["LDS_CACHE_BUCKET"]
aws_roles_config: str = configuration["AWS_ROLES_CONFIG"]
temp_folder: str = mkdtemp()
