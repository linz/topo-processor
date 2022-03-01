import os
import shutil

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.aws.aws_files import is_s3_path
from topo_processor.stac.validation import validate_stac
from topo_processor.util.configuration import temp_folder
from topo_processor.util.time import time_in_ms


@click.command()
@click.option(
    "-i",
    "--item",
    is_flag=True,
    help="Use item to validate items only.",
)
@click.option(
    "-c",
    "--collection",
    is_flag=True,
    help="Use collection to validate collections only.",
)
@click.option(
    "--metadata",
    required=False,
    help="(OPTIONAL) The path of the metadata csv file to validate.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs (it might be slower).",
)
def main(item: bool, collection: bool, metadata: str, verbose: str) -> None:
    if verbose:
        set_level(LogLevel.trace)
    else:
        set_level(LogLevel.info)

    start_time = time_in_ms()

    if metadata:
        if not is_s3_path(metadata):
            metadata = os.path.abspath(metadata)

    if item == collection:
        validate_stac(metadata)
    else:
        validate_stac(metadata, item, collection)

    # Cleanup
    shutil.rmtree(temp_folder)

    get_log().info(
        "validate completed",
        duration=time_in_ms() - start_time,
    )
