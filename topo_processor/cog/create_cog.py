import os

from topo_processor.cog.command import Command


async def create_cog(input_file: str, output_dir: str, compression_method: str) -> str:
    output_file = os.path.join(output_dir, f"{os.path.basename(input_file)}.{compression_method}.cog.tiff")

    gdal_translate = to_gdal_command(input_file, output_file, compression_method)
    await gdal_translate.run()
    return output_file


def to_gdal_command(input_file: str, output_file: str, compression_method: str):

    cmd = Command("gdal_translate", {"container": "osgeo/gdal", "tag": "ubuntu-small-latest"})
    cmd.mount(input_file)
    cmd.mount(os.path.dirname(output_file))
    cmd.arg(input_file)
    cmd.arg("-of", "COG")
    cmd.arg("-co", f"COMPRESS={compression_method}")
    cmd.arg("-co", "NUM_THREADS=ALL_CPUS")
    cmd.arg("-co", "PREDICTOR=2")
    cmd.arg(output_file)
    return cmd
