import os

from dotenv import dotenv_values

configuration = dotenv_values(".env")

aws_role_config_path = os.path.expanduser(configuration["AWS_ROLES_CONFIG"])
