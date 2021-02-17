import os
from typing import List

from topo_processor.cog.command import Command


async def create_cog(input_file: str, output_dir: str, compression_method: str):

    gdal_translate = to_gdal_command(input_file, output_dir, compression_method)
    await gdal_translate.run()


def to_gdal_command(input_file: str, output_dir: str, compression_method: str):
    output_file = os.path.join(output_dir, f"{os.path.basename(input_file)}.{compression_method}.cog.tiff")

    cmd = Command("gdal_translate", {"container": "osgeo/gdal", "tag": "ubuntu-small-latest"})
    cmd.mount(input_file)
    cmd.mount(output_dir)
    cmd.append_arg(input_file)
    cmd.append_arg("-of", "COG")
    cmd.append_arg("-co", f"COMPRESS={compression_method}")
    cmd.append_arg("-co", "NUM_THREADS=ALL_CPUS")
    cmd.append_arg("-co", "PREDICTOR=2")
    cmd.append_arg(output_file)
    return cmd
