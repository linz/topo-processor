import os
from functools import wraps

import click
import linz_logger
from linz_logger import LogLevel, get_log, logger, set_level

from topo_processor.file_system.get_fs import is_s3_path
from topo_processor.stac import DataType, collection_store, process_directory
from topo_processor.stac.item_factory import process_metadata
from topo_processor.util import time_in_ms
from topo_processor.util.transfer_collection import transfer_collection


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
def main(source, verbose):
    if verbose:
        set_level(LogLevel.trace)
    else:
        set_level(LogLevel.info)

    start_time = time_in_ms()

    if not is_s3_path(source):
        source = os.path.abspath(source)

    process_metadata(source)
    get_log().debug(
        "validate completed",
        file=source,
        duration=time_in_ms() - start_time,
    )
