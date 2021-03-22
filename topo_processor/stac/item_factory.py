import asyncio
import os

from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.metadata.metadata_loaders import metadata_loader_repo
from topo_processor.metadata.metadata_validators import metadata_validator_repo
from topo_processor.stac import DataType, Item
from topo_processor.stac.collection_store import get_collection
from topo_processor.util import time_in_ms


async def create_items(source_dir: str, data_type: DataType, target: str, temp_dir: str) -> None:
    start_time = time_in_ms()
    items_to_process = []
    for file_ in os.listdir(source_dir):
        source_path_path = os.path.join(source_dir, file_)
        item = Item(source_path_path, data_type, target, temp_dir)
        items_to_process.append(process_item(item))
    await asyncio.gather(*items_to_process)
    get_log().debug("Items Created", source_dir=source_dir, duration=time_in_ms() - start_time)


async def process_item(item):
    await metadata_loader_repo.load_metadata(item)
    if item.is_valid:
        await metadata_validator_repo.validate_metadata(item)
    if item.is_valid:
        await data_transformer_repo.transform_data(item)
    link_collection_item(item)


def link_collection_item(item):
    collection = get_collection(item.parent)
    if item.id in collection.items:
        raise Exception(f"Duplicate Items: {item.source_path}")
    item.collection = collection
    collection.items[item.id] = item
