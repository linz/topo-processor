from os import environ, path
from tempfile import mkdtemp

from dotenv import load_dotenv

load_dotenv()
lds_cache_bucket: str = environ.get("LDS_CACHE_BUCKET")
aws_role_config_path: str = path.expanduser(environ.get("AWS_ROLES_CONFIG"))
temp_folder: str = mkdtemp()
