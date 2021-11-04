from typing import Any, Dict, List, Union

from linz_logger import get_log

from topo_processor.metadata.metadata_loaders import metadata_loader_imagery_historic
from topo_processor.metadata.metadata_validators import metadata_validator_stac
from topo_processor.stac.validate_report import ValidateReport
from topo_processor.util import time_in_ms

from .collection import Collection
from .item import Item
from .store import collection_store, item_store


def validate_stac(metadata_file: str, validate_item: bool = True, validate_collection: bool = True) -> None:
    start_time = time_in_ms()
    item_report: ValidateReport = ValidateReport()
    collection_report: ValidateReport = ValidateReport()

    # Load metadata from metadata csv file
    metadata_loader_imagery_historic.load_all_metadata(metadata_file)
    get_log().debug("Metadata Loaded", metadata_file=metadata_file, duration=time_in_ms() - start_time)

    # Validate metadata from stored STAC objects
    if validate_item:
        item_report = validate_store(item_store)
        item_report.build_report()
    if validate_collection:
        collection_report = validate_store(collection_store)
        collection_report.build_report()

    # Print report
    # FIXME: case when only item or only collection
    get_log().info(
        "Metadata Validated",
        metadata_file=metadata_file,
        nbItemsValidated=item_report.total,
        nbCollectionsValidated=collection_report.total,
        duration=time_in_ms() - start_time,
        itemErrors=item_report.report_per_error_type,
        collectionErrors=collection_report.report_per_error_type,
    )


def validate_store(store: Union[list(Item), list(Collection)]) -> ValidateReport:
    validate_report: ValidateReport = ValidateReport()

    for stac_object in store.values():
        if stac_object.is_valid():
            validate_report.add_errors(metadata_validator_stac.validate_metadata_with_report(stac_object))

    return validate_report
