import asyncio
from functools import wraps

import click
from linz_logger import get_log

from topo_processor.metadata import DataType, create_collection
from topo_processor.uploader import upload_to_local_disk, upload_to_s3
from topo_processor.util.time import time_in_ms


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
@coroutine
async def main(source, datatype, target, upload):
    collection = await create_collection(source, DataType(datatype))
    start_time = time_in_ms()
    if upload:
        await upload_to_s3(collection, target)
    else:
        await upload_to_local_disk(collection, target)
    get_log().debug(
        "Upload Completed",
        location=target,
        data_type=collection.data_type.value,
        duration=time_in_ms() - start_time,
    )
