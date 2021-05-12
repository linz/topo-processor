import os

from topo_processor.cog.command import Command
from topo_processor.util.aws_credentials import get_credentials


def create_cog(input_path: str, output_path: str, compression_method: str) -> str:
    cmd = Command("gdal_translate", {"container": "osgeo/gdal", "tag": "ubuntu-small-latest"})
    if input_path.startswith("/vsis3"):
        cmd.env(f"AWS_ACCESS_KEY_ID={get_credentials().access_key}")
        cmd.env(f"AWS_SECRET_ACCESS_KEY={get_credentials().secret_key}")
        cmd.env(f"AWS_SESSION_TOKEN={get_credentials().token}")
    cmd.mount(input_path)
    cmd.mount(os.path.dirname(output_path))
    cmd.arg(input_path)
    cmd.arg("-of", "COG")
    cmd.arg("-co", f"COMPRESS={compression_method}")
    cmd.arg("-co", "NUM_THREADS=ALL_CPUS")
    cmd.arg("-co", "PREDICTOR=2")
    cmd.arg(output_path)
    return cmd
