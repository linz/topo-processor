import os

from topo_processor.metadata.loaders import repo

from .collection import Collection
from .data_type import DataType
from .item import Item


def create_collection(path: str, data_type: DataType) -> Collection:
    collection = Collection("title", "description", "license", data_type)
    create_item(collection, path)
    return collection


def create_item(collection: Collection, path: str) -> None:
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        item = Item(file_path, collection)
        repo.add_metadata(item)
        collection.items.append(item)
