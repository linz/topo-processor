import asyncio
import os

from linz_logger import get_log

from topo_processor.imagery.compressors import compressor_repo
from topo_processor.metadata.loaders import loader_repo
from topo_processor.metadata.validators import validator_repo
from topo_processor.util.time import time_in_ms

from .collection import Collection
from .data_type import DataType
from .item import Item


async def create_collection(path: str, data_type: DataType) -> Collection:
    start_time = time_in_ms()
    collection = Collection(data_type)
    await create_items(collection, path)
    get_log().debug(
        "Collection Created", id=collection.stac_collection.id, data_type=data_type, duration=time_in_ms() - start_time
    )
    return collection


async def process_item(item):
    await loader_repo.add_metadata(item)
    await validator_repo.check_validity(item)
    await compressor_repo.compress_data(item)


async def create_items(collection: Collection, path: str) -> None:
    start_time = time_in_ms()
    items_to_process = []
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        item = Item(file_path, collection)
        items_to_process.append(process_item(item))
        collection.items.append(item)
    await asyncio.gather(*items_to_process)
    get_log().debug("Items Created", count=len(collection.items), path=path, duration=time_in_ms() - start_time)


async def process_item(item):
    await loader_repo.add_metadata(item)
    await validator_repo.check_validity(item)
