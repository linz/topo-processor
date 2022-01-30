import os

import click
from linz_logger import LogLevel, get_log, set_level

from topo_processor.stac.data_type import DataType
from topo_processor.stac.item_factory import process_directory
from topo_processor.stac.store import collection_store
from topo_processor.util.aws_credentials import bucket_roles
from topo_processor.util.configuration import lds_cache_bucket
from topo_processor.util.s3 import bucket_name_from_path, is_s3_path
from topo_processor.util.time import time_in_ms
from topo_processor.util.transfer_collection import transfer_collection


@click.command()
@click.option(
    "-s",
    "--source",
    required=True,
    help="The name of the directory with data to import",
)
@click.option(
    "-rr",
    "--readrole",
    required=False,
    help="The AWS read role for the source bucket.",
)
@click.option(
    "-lr",
    "--ldscacherole",
    required=False,
    help="The AWS read role for the LDS Cache.",
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
    "-wr",
    "--writerole",
    required=False,
    help="The AWS write role for the target bucket.",
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
    "-v",
    "--verbose",
    is_flag=True,
    help="Use verbose to display trace logs",
)
def main(
    source: str, readrole: str, ldscacherole: str, datatype: str, correlationid: str, target: str, writerole: str, verbose: str
) -> None:
    if correlationid:
        get_log().info({"Correlation ID": correlationid})

    # Loads the roles
    if readrole:
        bucket_roles[bucket_name_from_path(source)] = {"roleArn": readrole}
    if ldscacherole:
        bucket_roles[lds_cache_bucket] = {"roleArn": ldscacherole}
    if writerole:
        bucket_roles[bucket_name_from_path(target)] = {"roleArn": writerole}

    if verbose:
        set_level(LogLevel.trace)

    start_time = time_in_ms()
    data_type = DataType(datatype)

    if not is_s3_path(source):
        source = os.path.abspath(source)

    process_directory(source, data_type)

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
