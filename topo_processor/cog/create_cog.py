import os

from topo_processor.cog.command import Command


def create_cog(input_path: str, output_path: str, compression_method: str) -> str:
    cmd = Command("gdal_translate", {"container": "osgeo/gdal", "tag": "ubuntu-small-latest"})
    cmd.mount(input_path)
    cmd.mount(os.path.dirname(output_path))
    cmd.arg(input_path)
    cmd.arg("-of", "COG")
    cmd.arg("-co", f"COMPRESS={compression_method}")
    cmd.arg("-co", "NUM_THREADS=ALL_CPUS")
    cmd.arg("-co", "PREDICTOR=2")
    cmd.arg(output_path)
    return cmd
