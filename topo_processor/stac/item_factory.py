import asyncio

from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.file_system.get_fs import get_fs, is_s3_path
from topo_processor.metadata.metadata_loaders import metadata_loader_repo
from topo_processor.metadata.metadata_validators import metadata_validator_repo
from topo_processor.stac.store import get_asset, item_store
from topo_processor.util import time_in_ms


async def process_directory(source_dir: str) -> None:
    start_time = time_in_ms()
    await _create_assets(source_dir)
    get_log().debug("Assets Created", source_dir=source_dir, duration=time_in_ms() - start_time)
    await _create_items()
    get_log().debug("Items Created", source_dir=source_dir, duration=time_in_ms() - start_time)


async def _create_assets(source_dir: str) -> None:
    assets_to_process = []
    fs = get_fs(source_dir)
    for (path, _, files) in fs.walk(source_dir):
        if not files:
            continue
        for file_ in files:
            if is_s3_path(source_dir):
                asset = get_asset(f"s3://{path}/{file_}")
            else:
                asset = get_asset(f"{path}/{file_}")
            assets_to_process.append(metadata_loader_repo.load_metadata(asset))
    await asyncio.gather(*assets_to_process)


async def _create_items():
    items_to_process = []
    for item in item_store.values():
        items_to_process.append(_process_item(item))
    await asyncio.gather(*items_to_process)


async def _process_item(item):
    if item.is_valid():
        await metadata_validator_repo.validate_metadata(item)
    if item.is_valid():
        await data_transformer_repo.transform_data(item)
