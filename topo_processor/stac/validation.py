import os
from typing import List, Union

from linz_logger import get_log

import topo_processor.stac.lds_cache as lds_cache
from topo_processor.file_system.get_fs import is_s3_path
from topo_processor.metadata.metadata_loaders import metadata_loader_imagery_historic
from topo_processor.metadata.metadata_validators import metadata_validator_stac
from topo_processor.stac.validate_report import ValidateReport
from topo_processor.util import time_in_ms
from topo_processor.util.aws_files import s3_download
from topo_processor.util.configuration import temp_folder
from topo_processor.util.gzip import decompress_file, is_gzip_file

from .collection import Collection
from .item import Item
from .store import collection_store, item_store


def validate_stac(metadata_file: str = "", validate_item: bool = True, validate_collection: bool = True) -> None:
    """This function only validate the Historical Imagery layer at the moment."""
    start_time = time_in_ms()
    item_report: ValidateReport = ValidateReport()
    collection_report: ValidateReport = ValidateReport()

    get_log().debug("validate_stac", layer=metadata_loader_imagery_historic.layer_id)

    if not metadata_file:
        metadata_file = lds_cache.get_layer(metadata_loader_imagery_historic.layer_id)
    else:
        if is_s3_path(metadata_file):
            local_metadata_file = temp_folder + "/" + os.path.basename(metadata_file)
            s3_download(metadata_file, local_metadata_file)
            metadata_file = local_metadata_file
        if is_gzip_file(metadata_file):
            decompress_file(metadata_file)

    # Load metadata from metadata csv file
    metadata_loader_imagery_historic.load_all_metadata(metadata_file)
    get_log().debug("Metadata Loaded", metadata_file=metadata_file, duration=time_in_ms() - start_time)

    # Validate metadata from stored STAC objects
    if validate_item:
        item_report = validate_store(item_store)
    if validate_collection:
        collection_report = validate_store(collection_store)

    # Print report
    get_log().info(
        "Metadata Validated",
        metadata_file=metadata_file,
        nbItemsValidated=item_report.total,
        nbCollectionsValidated=collection_report.total,
        duration=time_in_ms() - start_time,
        itemErrors=item_report.report_per_error_type,
        collectionErrors=collection_report.report_per_error_type,
    )


def validate_store(store: List[Union[Item, Collection]]) -> ValidateReport:
    validate_report: ValidateReport = ValidateReport()

    for stac_object in store.values():
        if stac_object.is_valid():
            validate_report.add_errors(metadata_validator_stac.validate_metadata_with_report(stac_object))

    return validate_report
