from datetime import datetime
from typing import List, TypedDict

import pystac as stac

from .collection import Collection


class Asset(TypedDict):
    temp_path: str
    key: str
    href: str
    properties = dict
    media_type = stac.MediaType
    stac_extensions = []
    content_type = str


class Item:

    source_path: str
    metadata_path: str
    id_: str
    gemoetry: str
    bbox: str
    datetime: datetime
    properties: dict
    stac_extensions: List[str]
    assets: List[Asset]
    content_type: str

    def __init__(self, source_path: str, collection: Collection):
        self.source_path = source_path
        self.properties = {}
        self.collection = collection
        self.stac_extensions = []
        self.assets = []
        self.content_type = "application/json"

    def add_asset(self, asset: Asset):
        self.assets.append(asset)
        for asset_stac_extension in asset["stac_extensions"]:
            if asset_stac_extension not in self.stac_extensions:
                self.stac_extensions.append(asset_stac_extension)

    def create_stac(self) -> stac.Item:
        stac_item = stac.Item(
            id=self.id_,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties=self.properties,
            stac_extensions=self.stac_extensions,
        )
        for asset in self.assets:
            stac_item.add_asset(
                key=asset["key"],
                asset=stac.Asset(href=asset["href"], properties=asset["properties"], media_type=asset["media_type"]),
            )
        return stac_item
