from datetime import datetime
from typing import List, TypedDict

import pystac

from .collection import Collection


class Asset(TypedDict):
    path: str
    key: str
    href: str
    properties = dict
    content_type = pystac.MediaType
    stac_extensions = []


class Item:

    source_path: str
    metadata_path: str
    id: str
    gemoetry: str
    bbox: str
    datetime: datetime
    properties: dict
    stac_extensions: List[str]
    assets: List[Asset]
    content_type: str
    is_valid: bool

    def __init__(self, source_path: str, collection: Collection):
        self.source_path = source_path
        self.metadata_path = None  # The RELATIVE path of the json file
        self.properties = {}
        self.collection = collection
        self.stac_extensions = []
        self.assets = []
        self.content_type = "application/json"
        self.is_valid = True

    def add_asset(self, asset: Asset):
        self.assets.append(asset)
        for asset_stac_extension in asset["stac_extensions"]:
            if asset_stac_extension not in self.stac_extensions:
                self.stac_extensions.append(asset_stac_extension)

    def create_stac(self) -> pystac.Item:
        stac_item = pystac.Item(
            id=self.id,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties=self.properties,
            stac_extensions=self.stac_extensions,
        )
        for asset in self.assets:
            stac_item.add_asset(
                key=asset["key"],
                asset=pystac.Asset(href=asset["href"], properties=asset["properties"], media_type=asset["content_type"]),
            )
        return stac_item
