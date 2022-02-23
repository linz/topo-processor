import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.lds_cache.lds_cache import get_metadata
from topo_processor.stac.item_factory import process_source
from topo_processor.stac.store import collection_store
from topo_processor.util.time import time_in_ms
from topo_processor.util.transfer_collection import transfer_collection


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The source of the data to import",
)
@click.option(
    "-d",
    "--datatype",
    required=True,
    type=click.Choice([data_type for data_type in DataType], case_sensitive=True),
    help="The datatype of the upload",
)
@click.option(
    "-t",
    "--target",
    required=True,
    help="The target directory path or bucket name of the upload",
)
@click.option(
    "-cid",
    "--correlationid",
    required=False,
    help="The correlation ID of the batch job",
)
@click.option(
    "-t",
    "--target",
    required=True,
    help="The target directory path or bucket name of the upload",
)
@click.option(
    "-m",
    "--metadata",
    required=False,
    help="The metadata file path",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(source: str, datatype: str, correlationid: str, target: str, metadata: str, verbose: str) -> None:
    get_log().info("upload_start", correlationId=correlationid, source=source, target=target, dataType=datatype)

    if verbose:
        set_level(LogLevel.trace)

    start_time = time_in_ms()
    data_type = DataType(datatype)

    # Caching the metadata required by the user.
    if metadata:
        get_metadata(data_type, None, metadata)

    process_source(source, data_type, metadata)

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
