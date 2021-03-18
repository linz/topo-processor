import os
from datetime import datetime
from mimetypes import MimeTypes
from typing import List

import pystac

from .asset import Asset
from .collection import Collection
from .data_type import DataType


class Item:
    source_path: str
    data_type: DataType
    target: str
    temp_dir: str
    metadata_path: str
    id: str
    gemoetry: str
    bbox: str
    datetime: datetime
    properties: dict
    stac_extensions: dict
    assets: List[Asset]
    content_type: pystac.MediaType
    file_ext: str
    is_valid: bool
    collection: Collection

    def __init__(self, source_path: str, data_type: DataType, target: str, temp_dir: str):
        self.source_path = source_path
        self.data_type = data_type
        self.target = target
        self.temp_dir = temp_dir
        self.metadata_path = None  # The RELATIVE path of the json file
        self.properties = {}
        self.stac_extensions = ["file"]
        self.content_type = pystac.MediaType.JSON
        self.file_ext = MimeTypes().guess_extension(self.content_type)
        self.is_valid = True
        self.assets = {
            "source": Asset(
                key="source",
                path=source_path,
                content_type=MimeTypes().guess_type(source_path)[0],
                file_ext=os.path.splitext(source_path)[1],
                needs_upload=True,
            )
        }

    def add_asset(self, descriptor: str, asset: Asset):
        self.assets[descriptor] = asset

    def create_stac(self) -> pystac.Item:
        stac = pystac.Item(
            id=self.id,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties=self.properties,
            stac_extensions=self.stac_extensions,
        )
        existing_asset_hrefs = {}
        for asset in self.assets.values():
            if not asset.needs_upload:
                continue

            asset.href = f"./{self.collection.title}/{self.id}{asset.file_ext}"
            if asset.href in existing_asset_hrefs:
                raise Exception(f"{asset.href} already exists.")

            stac.add_asset(key=asset.key, asset=asset.create_stac())
            existing_asset_hrefs[asset.href] = asset
        return stac
