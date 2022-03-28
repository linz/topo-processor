import click
import pystac
from linz_logger import LogLevel, get_log, set_level

from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.lds_cache.lds_cache import get_metadata
from topo_processor.stac.item_factory import process_source
from topo_processor.stac.iter_errors_validator import IterErrorsValidator
from topo_processor.stac.store import collection_store
from topo_processor.util.s3 import is_s3_path
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
@click.option(
    "-f",
    "--footprint",
    required=False,
    help="The survey footprint metadata path",
)
def main(source: str, datatype: str, correlationid: str, target: str, metadata: str, verbose: str, footprint: str) -> None:
    get_log().info("upload_start", correlationId=correlationid, source=source, target=target, dataType=datatype)
    try:
        pystac.validation.set_validator(IterErrorsValidator())

        if verbose:
            set_level(LogLevel.trace)

        start_time = time_in_ms()
        data_type = DataType(datatype)

        # Caching the metadata required by the user.
        if metadata:
            get_metadata(data_type, None, metadata)
            if not is_s3_path(metadata):
                if not footprint:
                    get_log().error(
                        "survey_footprint_metadata_not_given",
                        msg="You have to provide a local path for the survey footprint metadata",
                    )
                    raise Exception("survey footprint metadata not given")
                else:
                    if data_type == DataType.IMAGERY_HISTORIC:
                        get_metadata(DataType.SURVEY_FOOTPRINT_HISTORIC, None, footprint)
                    else:
                        raise Exception("Not yet implemented")

        process_source(source, data_type, metadata)

        for collection in collection_store.values():
            transfer_collection(collection, target)

        get_log().debug(
            "Job Completed",
            source=source,
            location=target,
            correlationid=correlationid,
            data_type=data_type,
            duration=time_in_ms() - start_time,
        )
    except Exception as e:
        get_log().error("Job Failed", error=e, source=source, correlationid=correlationid, data_type=datatype)
    finally:
        for collection in collection_store.values():
            collection.delete_temp_dir()
