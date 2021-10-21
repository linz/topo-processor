from typing import Dict
from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.file_system.get_fs import get_fs
from topo_processor.file_system.get_path_with_protocol import get_path_with_protocol
from topo_processor.metadata.metadata_loaders import metadata_loader_repo, metadata_loader_imagery_historic
from topo_processor.metadata.metadata_validators import metadata_validator_repo, metadata_validator_stac
from topo_processor.stac.store import get_asset, item_store
from topo_processor.util import time_in_ms


def process_directory(source_dir: str) -> None:
    start_time = time_in_ms()
    _create_assets(source_dir)
    get_log().debug("Assets Created", source_dir=source_dir, duration=time_in_ms() - start_time)
    _create_items()
    get_log().debug("Items Created", source_dir=source_dir, duration=time_in_ms() - start_time)


def process_metadata(metadata_file: str) -> None:
    start_time = time_in_ms()
    errors_per_item: Dict[str, Dict[str, list]] = {}
    errors_per_type: Dict[str, Dict[str, int]] = {}
    total_items_processed = 0

    # Load metadata from metadata csv file
    metadata_loader_imagery_historic.load_all_metadata(metadata_file)
    get_log().debug("Metadata Loaded", metadata_file=metadata_file, duration=time_in_ms() - start_time)

    # Validate item against schema
    for item in item_store.values():
        if item.is_valid():
            errors_per_item[item.id] = metadata_validator_stac.validate_metadata_with_report(item)
            total_items_processed = total_items_processed + 1

    # Build errors report
    for errors_item in errors_per_item.values():
        for schema_uri in errors_item:
            if schema_uri not in errors_per_type:
                errors_per_type[schema_uri] = {}
            for error in errors_item[schema_uri]:
                if error in errors_per_type[schema_uri]:
                    errors_per_type[schema_uri][error] = errors_per_type[schema_uri][error] + 1
                else:
                    errors_per_type[schema_uri][error] = 1

    get_log().info(
        "Metadata Validated",
        metadata_file=metadata_file,
        nbItemsProcessed=total_items_processed,
        duration=time_in_ms() - start_time,
        errors=errors_per_type,
    )


def _create_assets(source_dir: str) -> None:
    assets_to_process = []
    fs = get_fs(source_dir)
    for (path, _, files) in fs.walk(source_dir):
        if not files:
            continue
        for file_ in files:
            asset_path = get_path_with_protocol(source_dir, fs, path)
            asset = get_asset(f"{asset_path}/{file_}")
            assets_to_process.append(metadata_loader_repo.load_metadata(asset))


def _create_items():
    items_to_process = []
    for item in item_store.values():
        items_to_process.append(_process_item(item))


def _process_item(item):
    if item.is_valid():
        metadata_validator_repo.validate_metadata(item)
    if item.is_valid():
        data_transformer_repo.transform_data(item)
