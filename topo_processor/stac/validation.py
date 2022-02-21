from typing import Dict, Union

from linz_logger import get_log

from topo_processor.metadata.data_type import DataType, get_layer_id
from topo_processor.metadata.metadata_loaders import metadata_loader_imagery_hist
from topo_processor.metadata.metadata_validators import metadata_validator_stac
from topo_processor.stac.validate_report import ValidateReport
from topo_processor.util.time import time_in_ms

from .collection import Collection
from .item import Item
from .store import collection_store, item_store


def validate_stac(metadata_file: str = "", validate_item: bool = True, validate_collection: bool = True) -> None:
    """This function only validate the Historical Imagery layer at the moment."""
    # FIXME: Make this function generic by validating other layers (vs only Historical Imagery atm)
    start_time = time_in_ms()
    item_report: ValidateReport = ValidateReport()
    collection_report: ValidateReport = ValidateReport()

    get_log().debug("validate_stac", layer=get_layer_id(DataType.IMAGERY_HISTORIC))

    # Load metadata from metadata csv file
    metadata_loader_imagery_hist.load_metadata(None, metadata_file, True)
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


def validate_store(store: Union[Dict[str, Item], Dict[str, Collection]]) -> ValidateReport:
    validate_report: ValidateReport = ValidateReport()

    for stac_object in store.values():
        if stac_object.is_valid():
            validate_report.add_errors(metadata_validator_stac.validate_metadata_with_report(stac_object))

    return validate_report
