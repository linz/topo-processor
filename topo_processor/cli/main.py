import asyncio
from functools import wraps

import click
import pystac as stac

from topo_processor.metadata import DataType, create_collection


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
    required=False,
    is_flag=True,
    help="Upload files to local file system or AWS",
)
@click.option("--dry-run", is_flag=True, help="Run code without performing any upload")
@coroutine
async def main(source, datatype, target, dry_run):
    collection = await create_collection(source, DataType(datatype))
    for item in collection.items:
        stac.write_file(obj=item.stac_item, include_self_link=True, dest_href="build/{}".format(item.output_filename))
