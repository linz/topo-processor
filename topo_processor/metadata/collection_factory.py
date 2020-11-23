import asyncio
import os

from linz_logger import get_log

from topo_processor.metadata.loaders import repo
from topo_processor.util.time import time_in_ms

from .collection import Collection
from .data_type import DataType
from .item import Item


async def create_collection(path: str, data_type: DataType) -> Collection:
    start_time = time_in_ms()
    collection = Collection("title", "description", "license", data_type)
    await create_items(collection, path)
    get_log().debug("Collection Loaded", title=collection.title, data_type=data_type, duration=time_in_ms() - start_time)
    return collection


async def create_items(collection: Collection, path: str) -> None:
    list_to_add_metadata = []
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        item = Item(file_path, collection)
        list_to_add_metadata.append(repo.add_metadata(item))
        collection.items.append(item)
    await asyncio.gather(*list_to_add_metadata)
