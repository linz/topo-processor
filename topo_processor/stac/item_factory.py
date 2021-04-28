import asyncio
from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.metadata.metadata_validators import metadata_validator_repo
from topo_processor.stac.store import item_store
from topo_processor.util import time_in_ms
from topo_processor.file_system import get_file_system

async def process_directory(directory) -> None:
    fs = get_file_system(directory)
    await fs.read(directory)
    await _create_items()

async def _create_items():
    start_time = time_in_ms()
    items_to_process = []
    for item in item_store.values():
        items_to_process.append(_process_item(item))
    await asyncio.gather(*items_to_process)
    get_log().debug("Items Created", duration=time_in_ms() - start_time)

async def _process_item(item):
    if item.is_valid():
        await metadata_validator_repo.validate_metadata(item)
    if item.is_valid():
        await data_transformer_repo.transform_data(item)
