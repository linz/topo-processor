import asyncio
import os

from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
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
    for file_ in os.listdir(source_dir):
        path = os.path.join(source_dir, file_)
        asset = get_asset(path)
        assets_to_process.append(metadata_loader_repo.load_metadata(asset))
    await asyncio.gather(*assets_to_process)


async def _create_items():
    items_to_process = []
    for item in item_store.values():
        items_to_process.append(_process_item(item))
    await asyncio.gather(*items_to_process)


async def _process_item(item):
    if item.check_validity:
        await metadata_validator_repo.validate_metadata(item)
    if item.check_validity:
        await data_transformer_repo.transform_data(item)
