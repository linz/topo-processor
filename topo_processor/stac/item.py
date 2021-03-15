from datetime import datetime
from mimetypes import MimeTypes
from typing import List

import pystac

from .asset import Asset
from .collection import Collection


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
    content_type: pystac.MediaType
    file_ext: str
    is_valid: bool

    def __init__(self, source_path: str, collection: Collection):
        self.source_path = source_path
        self.metadata_path = None  # The RELATIVE path of the json file
        self.properties = {}
        self.collection = collection
        self.stac_extensions = ["file"]
        self.assets = []
        self.content_type = pystac.MediaType.JSON
        self.file_ext = MimeTypes().guess_extension(self.content_type)
        self.is_valid = True

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def create_stac(self) -> pystac.Item:
        stac = pystac.Item(
            id=self.id,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties=self.properties,
            stac_extensions=self.stac_extensions,
        )
        for asset in self.assets:
            stac.add_asset(
                key=asset.key,
                asset=asset.create_stac(),
            )
        return stac
