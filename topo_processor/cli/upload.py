import os

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.file_system.get_fs import is_s3_path
from topo_processor.metadata.metadata_loaders import metadata_loader_imagery_historic
from topo_processor.stac import DataType, collection_store, lds_cache, process_directory
from topo_processor.util import time_in_ms
from topo_processor.util.transfer_collection import transfer_collection


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The name of the directory with data to import",
)
@click.option(
    "-d",
    "--datatype",
    required=True,
    type=click.Choice([data_type for data_type in DataType], case_sensitive=True),
    help="The Datatype of the upload",
)
@click.option(
    "-t",
    "--target",
    required=True,
    help="The target directory path or bucket name of the upload",
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
    help="Use verbose to display trace logs",
)
def main(source, datatype, target, metadata, verbose):
    if verbose:
        set_level(LogLevel.trace)

    start_time = time_in_ms()
    data_type = DataType(datatype)

    if not metadata:
        metadata = lds_cache.get_layer(metadata_loader_imagery_historic.layer_id)

    if not is_s3_path(source):
        source = os.path.abspath(source)

    process_directory(source, metadata)

    try:
        for collection in collection_store.values():
            transfer_collection(collection, target)

    finally:
        for collection in collection_store.values():
            collection.delete_temp_dir()
        get_log().debug(
            "Job Completed",
            location=target,
            data_type=data_type,
            duration=time_in_ms() - start_time,
        )
