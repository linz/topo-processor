import os

from topo_processor.cog.command import Command
from topo_processor.file_system.get_fs import bucket_name_from_path, is_s3_path
from topo_processor.util.aws_credentials import Credentials, get_credentials


def create_cog(input_path: str, output_path: str, compression_method: str, overview_compression_method: str) -> str:
    cmd = Command("gdal_translate", {"container": "osgeo/gdal", "tag": "ubuntu-small-latest"})
    if is_s3_path(input_path):
        credentials: Credentials = get_credentials(bucket_name_from_path(input_path))
        cmd.env(f"AWS_ACCESS_KEY_ID={credentials.access_key}")
        cmd.env(f"AWS_SECRET_ACCESS_KEY={credentials.secret_key}")
        cmd.env(f"AWS_SESSION_TOKEN={credentials.token}")
        input_path = f"/vsis3/{input_path.replace('s3://', '')}"

    cmd.mount(input_path)
    cmd.mount(os.path.dirname(output_path))
    cmd.arg(input_path)
    cmd.arg("-of", "COG")
    cmd.arg("-co", f"COMPRESS={compression_method}")
    cmd.arg("-co", "NUM_THREADS=ALL_CPUS")
    cmd.arg("-co", "PREDICTOR=2")
    cmd.arg("-co", f"OVERVIEW_COMPRESS={overview_compression_method}")
    cmd.arg("-co", "BIGTIFF=YES")
    cmd.arg("-co", "OVERVIEW_RESAMPLING=LANCZOS")
    cmd.arg("-co", "BLOCKSIZE=512")
    cmd.arg("-co", "OVERVIEW_QUALITY=90")
    cmd.arg("-co", "SPARSE_OK=TRUE")
    cmd.arg(output_path)
    return cmd
