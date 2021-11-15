import os

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.stac.data_type import DataType
from topo_processor.stac.validation import validate_stac
from topo_processor.util import time_in_ms
from topo_processor.util.configuration import lds_cache_local_tmp_folder
from topo_processor.util.files import empty_dir


@click.command()
@click.option(
    "-l",
    "--layer",
    required=False,
    help="The layer number to validate. Take the last version by default.",
)
@click.option(
    "-v",
    "--version",
    required=False,
    help="(OPTIONAL) The specific version number to validate.",
)
@click.option(
    "-s",
    "--source",
    required=False,
    help="The path of the local metadata csv file to validate.",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Use debug to display trace logs (it might be slower).",
)
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
def main(layer, version, source, debug, item, collection):
    if debug:
        set_level(LogLevel.trace)
    else:
        set_level(LogLevel.info)

    start_time = time_in_ms()

    if source:
        source = os.path.abspath(source)

    if item == collection:
        validate_stac(layer, version, source)
    else:
        validate_stac(layer, version, source, item, collection)

    # Cleanup
    empty_dir(os.path.abspath(os.path.join(os.getcwd(), lds_cache_local_tmp_folder)))

    get_log().info(
        "validate completed",
        layer=layer,
        dataVersion=version,
        metadataFile=source,
        duration=time_in_ms() - start_time,
    )
