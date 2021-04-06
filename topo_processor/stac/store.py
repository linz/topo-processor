from .asset import Asset
from .collection import Collection
from .item import Item

collection_store = {}
item_store = {}
asset_store = {}


def get_collection(title: str) -> Collection:
    if title not in collection_store:
        collection = Collection(title)
        collection_store[title] = collection
    return collection_store[title]


def get_asset(source_path: str) -> Asset:
    if source_path not in asset_store:
        asset = Asset(source_path)
        asset_store[source_path] = asset
    return asset_store[source_path]


def get_item(item_id: str) -> Item:
    if item_id not in item_store:
        item = Item(item_id)
        item_store[item_id] = item
    return item_store[item_id]
