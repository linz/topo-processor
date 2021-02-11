import asyncio
import os

from linz_logger import get_log

from topo_processor.util.time import time_in_ms

TRANSLATE_ARGS = "-co NUM_THREADS=ALL_CPUS -co PREDICTOR=2"


def volume(input_dir: str, output_dir: str) -> list:
    volumes = []
    if input_dir.startswith(output_dir):
        volumes.append(output_dir)
    elif output_dir.startswith(input_dir):
        volumes.append(input_dir)
    elif output_dir == input_dir:
        volumes.append(input_dir)
    else:
        volumes.append(input_dir, output_dir)
    if len(volumes) == 1:
        return f"--volume {volumes[0]}:{volumes[0]}"
    else:
        return f"-- volumes {volumes[0]}:{volumes[0]} \
                 -- volumes {volumes[1]}:{volumes[1]}"


def docker_gdal(input_dir: str, output_dir: str) -> str:
    return f"docker run \
        --user {os.geteuid()}:{os.getegid()} \
        {volume(input_dir, output_dir)} \
        --rm \
        osgeo/gdal:ubuntu-small-latest $@"


async def create_cog(input_tiff_path, output_dir):
    start_time = time_in_ms()
    input_dir = os.path.dirname(input_tiff_path)
    output_cog_path = os.path.join(output_dir, f"{os.path.basename(input_tiff_path)}.tif.deflate.cog.tiff")
    cmd = f"{docker_gdal(input_dir, output_dir)} gdal_translate {input_tiff_path} -of COG -co COMPRESS=deflate \
            {TRANSLATE_ARGS} {output_cog_path}"
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if stderr:
        raise Exception(stderr.decode())
    get_log().debug(
        "Subprocess Created",
        stdout=stdout.decode(),
        duration=time_in_ms() - start_time,
    )
