import os

from linz_logger import get_log

from topo_processor.metadata.loaders import repo
from topo_processor.util.time import time_in_ms

from .collection import Collection
from .data_type import DataType
from .item import Item


def create_collection(path: str, data_type: DataType) -> Collection:
    start_time = time_in_ms()
    collection = Collection("title", "description", "license", data_type)
    create_item(collection, path)
    get_log().debug("CreateCollection", title=collection.title, data_type=data_type, duration=time_in_ms() - start_time)
    return collection


def create_item(collection: Collection, path: str) -> None:
    start_time = time_in_ms()
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        item = Item(file_path, collection)
        repo.add_metadata(item)
        collection.items.append(item)
    get_log().debug("CreateItem", path=path, duration=time_in_ms() - start_time)
