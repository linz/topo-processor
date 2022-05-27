import os

from topo_processor.cog.command import Command
from topo_processor.util.aws_credentials import Credentials, get_credentials_from_bucket
from topo_processor.util.s3 import bucket_name_from_path, is_s3_path


def create_cog(input_path: str, output_path: str) -> Command:
    is_s3 = is_s3_path(input_path)
    if is_s3:
        credentials: Credentials = get_credentials_from_bucket(bucket_name_from_path(input_path))
        input_path = f"/vsis3/{input_path.replace('s3://', '')}"
    if os.environ.get("IS_DOCKER") == "true":
        cmd = Command("gdal_translate")
        if is_s3:
            os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
            os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
            os.environ["AWS_SESSION_TOKEN"] = credentials.token
    else:
        cmd = Command("gdal_translate", {"container": "osgeo/gdal", "tag": "ubuntu-small-latest"})
        if is_s3:
            cmd.env(f"AWS_ACCESS_KEY_ID={credentials.access_key}")
            cmd.env(f"AWS_SECRET_ACCESS_KEY={credentials.secret_key}")
            cmd.env(f"AWS_SESSION_TOKEN={credentials.token}")

    cmd.env("GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR")
    cmd.mount(input_path)
    cmd.mount(os.path.dirname(output_path))
    cmd.arg(input_path)
    cmd.arg("-of", "COG")
    cmd.arg("-co", "COMPRESS=LZW")
    cmd.arg("-co", "NUM_THREADS=ALL_CPUS")
    cmd.arg("-co", "PREDICTOR=2")
    cmd.arg("-co", "OVERVIEW_COMPRESS=JPEG")
    cmd.arg("-co", "BIGTIFF=YES")
    cmd.arg("-co", "OVERVIEW_RESAMPLING=LANCZOS")
    cmd.arg("-co", "BLOCKSIZE=512")
    cmd.arg("-co", "OVERVIEW_QUALITY=90")
    cmd.arg("-co", "SPARSE_OK=TRUE")
    cmd.arg(output_path)
    return cmd
