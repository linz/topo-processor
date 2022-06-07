from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.file_system.assets import get_assets
from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.metadata_loaders import metadata_loader_rep
from topo_processor.metadata.metadata_validators import metadata_validator_repo
from topo_processor.stac.store import asset_store, item_store
from topo_processor.util.time import time_in_ms


def process_source(source: str, data_type: DataType, metadata_path: str = "", force: bool = False) -> None:
    start_time = time_in_ms()
    _create_assets(source, data_type, metadata_path)
    total_asset = len(asset_store)
    if total_asset == 0:
        get_log().warn("No Assets Found", assets=total_asset, source=source, duration=time_in_ms() - start_time)
        return

    get_log().debug("Assets Created", assets=total_asset, source=source, duration=time_in_ms() - start_time)

    start_time = time_in_ms()
    _create_items(force)
    total_item = len(item_store)
    if len(item_store) == 0:
        get_log().warn("No Items Created", items=total_item, source=source, duration=time_in_ms() - start_time)
        return

    get_log().debug("Items Created", items=total_item, source=source, duration=time_in_ms() - start_time)


def _create_assets(source: str, data_type: str, metadata_path: str) -> None:
    assets = get_assets(source, data_type, metadata_path)
    for asset in assets:
        metadata_loader_rep.load_metadata(asset)
        if not asset.item:
            raise Exception(f"No item set for asset. Process is stopped.")


def _create_items(force: bool = False) -> None:
    all_items_valid = True
    # Validate metadata of valid items
    # Item can be already detected invalid from the metadata loader
    # For those, we don't want to validate their metadata
    for item in item_store.values():
        if item.is_valid():
            metadata_is_valid = metadata_validator_repo.validate_metadata(item)
            if all_items_valid and not metadata_is_valid:
                all_items_valid = metadata_is_valid

    if not all_items_valid and not force:
        raise Exception("At least one Item is not valid. Process is stopped")

    for item in item_store.values():
        if item.is_valid():
            data_transformer_repo.transform_data(item)
