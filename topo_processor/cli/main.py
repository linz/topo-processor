import asyncio
import os
from functools import wraps

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.stac import DataType, collection_store, process_directory
from topo_processor.uploader import upload_to_local_disk, upload_to_s3
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
    help="The name of the directory with data to import",
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
    "-u",
    "--upload",
    is_flag=True,
    help="If True will be uploaded to the specified target s3 bucket otherwise will be stored locally in specified target location",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
@coroutine
async def main(source, datatype, target, upload, verbose):
    if verbose:
        set_level(LogLevel.trace)
    start_time = time_in_ms()
    source_dir = os.path.abspath(source)
    data_type = DataType(datatype)
    await process_directory(source_dir)
    try:
        for collection in collection_store.values():
            if upload:
                await upload_to_s3(collection, target)
            else:
                await upload_to_local_disk(collection, target)

    finally:
        for collection in collection_store.values():
            collection.delete_temp_dir()
        get_log().debug(
            "Upload Completed",
            location=target,
            data_type=data_type.value,
            duration=time_in_ms() - start_time,
        )
