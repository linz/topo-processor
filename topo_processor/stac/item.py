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


class Item:

    source_path: str
    metadata_path: str
    content_type: str
    assets: Asset
    id: str
    gemoetry: str
    bbox: str
    datetime: datetime

    properties: dict
    stac_extensions: List[str]

    def __init__(self, source_path: str, collection: Collection):
        self.source_path = source_path
        self.collection = collection
        self.properties = {}
        self.assets = []
        self.stac_extensions = []

    def add_asset(self, asset: Asset):
        self.assets.append(asset)
        for asset_stac_extension in asset["stac_extensions"]:
            if asset_stac_extension not in self.stac_extensions:
                self.stac_extensions.append(asset_stac_extension)
