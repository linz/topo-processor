import os
from tempfile import mkdtemp

from dotenv import dotenv_values

configuration = dotenv_values(".env")

lds_cache_bucket: str = configuration["LDS_CACHE_BUCKET"]
aws_role_config_path = os.path.expanduser(configuration["AWS_ROLES_CONFIG"])
temp_folder: str = mkdtemp()
