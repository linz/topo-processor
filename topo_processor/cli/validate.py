import os

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.file_system.get_fs import is_s3_path
from topo_processor.stac.validation import validate_stac
from topo_processor.util import time_in_ms


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The name of the metadata csv file to import",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
@click.option(
    "-i",
    "--item",
    is_flag=True,
    help="Use item to validate items only",
)
@click.option(
    "-c",
    "--collection",
    is_flag=True,
    help="Use collection to validate collections only",
)
def main(source, verbose, item, collection):
    if verbose:
        set_level(LogLevel.trace)
    else:
        set_level(LogLevel.info)

    start_time = time_in_ms()

    if not is_s3_path(source):
        source = os.path.abspath(source)

    if item == collection:
        validate_stac(source)
    else:
        validate_stac(source, item, collection)

    get_log().debug(
        "validate completed",
        file=source,
        duration=time_in_ms() - start_time,
    )
