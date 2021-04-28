import asyncio
import os
from functools import wraps

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.file_system import get_file_system
from topo_processor.stac import DataType, collection_store, process_directory
from topo_processor.util import time_in_ms


def coroutine(f):
    """
    There is no built in support for asyncio in click.
    This custom decorator allows it to be run.
    https://github.com/pallets/click/issues/85#issuecomment-503464628
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    type=click.Path(exists=True),
    help="The absolute path to the directory with data to import",
)
@click.option(
    "-d",
    "--datatype",
    required=True,
    type=click.Choice([data_type.value for data_type in DataType], case_sensitive=True),
    help="The Datatype of the upload",
)
@click.option(
    "-t",
    "--target",
    required=True,
    help="The target directory path or bucket name of the upload",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
@coroutine
async def main(source, datatype, target, verbose):
    if verbose:
        set_level(LogLevel.trace)
    start_time = time_in_ms()
    data_type = DataType(datatype)

    target_fs = get_file_system(target)

    await process_directory(source)

    try:
        for collection in collection_store.values():
            await target_fs.write(collection, target)
    finally:
        for collection in collection_store.values():
            collection.delete_temp_dir()
        get_log().debug(
            "Finished Job",
            location=target,
            data_type=data_type.value,
            duration=time_in_ms() - start_time,
        )
