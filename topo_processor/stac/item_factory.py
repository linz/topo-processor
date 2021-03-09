import asyncio
import os

from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.metadata.metadata_loaders import metadata_loader_repo
from topo_processor.metadata.metadata_validators import metadata_validator_repo
from topo_processor.stac import DataType, Item
from topo_processor.util.time import time_in_ms


async def create_items(source_dir: str, data_type: DataType, temp_dir: str) -> None:
    start_time = time_in_ms()
    items_to_process = []
    items = []
    for f in os.listdir(source_dir):
        source_file = os.path.join(source_dir, f)
        item = Item(source_file, data_type, temp_dir)
        items_to_process.append(process_item(item))
        items.append(item)
    await asyncio.gather(*items_to_process)
    get_log().debug("Items Created", data_type=data_type, source_dir=source_dir, duration=time_in_ms() - start_time)
    return items


async def process_item(item):
    await metadata_loader_repo.add_metadata(item)
    await metadata_validator_repo.validate_metadata(item)
    await data_transformer_repo.transform_data(item)
