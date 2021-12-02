from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.file_system.get_fs import get_fs
from topo_processor.file_system.get_path_with_protocol import get_path_with_protocol
from topo_processor.metadata.metadata_loaders import metadata_loader_repo
from topo_processor.metadata.metadata_validators import metadata_validator_repo
from topo_processor.stac.store import get_asset, item_store
from topo_processor.util import time_in_ms


def process_directory(source_dir: str, metadata_file: str) -> None:
    start_time = time_in_ms()
    _create_assets(source_dir, metadata_file)
    get_log().debug("Assets Created", source_dir=source_dir, duration=time_in_ms() - start_time)
    _create_items()
    get_log().debug("Items Created", source_dir=source_dir, duration=time_in_ms() - start_time)


def _create_assets(source_dir: str, metadata_file: str) -> None:
    fs = get_fs(source_dir)
    for (path, _, files) in fs.walk(source_dir):
        if not files:
            continue
        for file_ in files:
            asset_path = get_path_with_protocol(source_dir, fs, path)
            asset = get_asset(f"{asset_path}/{file_}")
            metadata_loader_repo.load_metadata(metadata_file, asset)


def _create_items() -> None:
    for item in item_store.values():
        _process_item(item)


def _process_item(item) -> None:
    if item.is_valid():
        metadata_validator_repo.validate_metadata(item)
    if item.is_valid():
        data_transformer_repo.transform_data(item)
