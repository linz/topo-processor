import json
import os
from typing import Dict

from dotenv import dotenv_values

configuration = dotenv_values(".env")

aws_roles_config: Dict = json.load(open(os.path.expanduser(configuration["AWS_ROLES_CONFIG"])))
