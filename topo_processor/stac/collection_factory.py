import asyncio
import os
from tempfile import mkdtemp

from linz_logger import get_log

from topo_processor.data.data_transformers import data_transformer_repo
from topo_processor.metadata.metadata_loaders import metadata_loader_repo
from topo_processor.metadata.metadata_validators import metadata_validator_repo
from topo_processor.util.time import time_in_ms

from .collection import Collection
from .data_type import DataType
from .item import Item


async def create_collection(source_dir: str, data_type: DataType) -> Collection:
    start_time = time_in_ms()
    temp_dir = mkdtemp()
    collection = Collection(data_type, temp_dir)
    await create_items(collection, source_dir)
    get_log().debug(
        "Collection Created", id=collection.stac_collection.id, data_type=data_type, duration=time_in_ms() - start_time
    )
    return collection


async def create_items(collection: Collection, source_dir: str) -> None:
    start_time = time_in_ms()
    items_to_process = []
    for file_ in os.listdir(source_dir):
        source_path_path = os.path.join(source_dir, file_)
        item = Item(source_path_path, collection)
        items_to_process.append(process_item(item))
        collection.items.append(item)
    await asyncio.gather(*items_to_process)
    get_log().debug("Items Created", count=len(collection.items), source_dir=source_dir, duration=time_in_ms() - start_time)


async def process_item(item):
    await metadata_loader_repo.add_metadata(item)
    await metadata_validator_repo.validate_metadata(item)
    await data_transformer_repo.transform_data(item)
