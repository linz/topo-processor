import os

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.file_system.get_fs import is_s3_path
from topo_processor.stac.validation import validate_stac
from topo_processor.util import time_in_ms
from topo_processor.util.configuration import lds_cache_local_tmp_folder
from topo_processor.util.files import empty_dir


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
def main(item, collection, metadata, verbose):
    if verbose:
        set_level(LogLevel.trace)
    else:
        set_level(LogLevel.info)

    start_time = time_in_ms()

    if metadata:
        if not is_s3_path(metadata):
            source = os.path.abspath(metadata)

    if item == collection:
        validate_stac(source)
    else:
        validate_stac(source, item, collection)

    # Cleanup
    empty_dir(os.path.abspath(os.path.join(os.getcwd(), lds_cache_local_tmp_folder)))

    get_log().info(
        "validate completed",
        layer=layer,
        dataVersion=version,
        metadataFile=source,
        duration=time_in_ms() - start_time,
    )
