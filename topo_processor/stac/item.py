import os
from datetime import datetime
from typing import List

import pystac

from topo_processor.util import Validity

from .asset import Asset
from .collection import Collection


class Item:

    id: str

    gemoetry: str
    bbox: str
    datetime: datetime
    properties: dict

    stac_extensions: set
    assets: List[Asset]
    collection: Collection

    valid: Validity

    def __init__(self, item_id: str):
        self.properties = {}
        self.id = item_id
        self.stac_extensions = set(["file"])
        self.valid = Validity()
        self.collection = None
        self.assets = []

    def get_tmp_dir(self):
        temp_dir = os.path.join(self.collection.get_temp_dir(), self.id)
        os.mkdir(temp_dir)
        return temp_dir

    def is_valid(self):
        if not self.valid.is_valid:
            return False
        for asset in self.assets:
            if not asset.valid.is_valid:
                return False
        return True

    def add_asset(self, asset: Asset):
        if asset.item:
            raise Exception(f"Asset is already assoiciated with an item: existing item='{asset.item.id}' new item='{self.id}'")
        self.assets.append(asset)
        asset.item = self

    def add_extension(self, ext: str):
        self.stac_extensions.add(ext)

    def create_stac(self) -> pystac.Item:
        stac = pystac.Item(
            id=self.id,
            geometry=None,
            bbox=None,
            datetime=datetime.now(),
            properties=self.properties,
            stac_extensions=list(self.stac_extensions),
        )
        existing_asset_hrefs = {}
        for asset in self.assets:
            if not asset.needs_upload:
                continue

            asset.href = f"./{self.collection.title}/{self.id}{asset.file_ext()}"
            if asset.href in existing_asset_hrefs:
                raise Exception(f"{asset.href} already exists.")

            stac.add_asset(
                key=(asset.get_content_type() if asset.get_content_type() else asset.file_ext()), asset=asset.create_stac()
            )
            existing_asset_hrefs[asset.href] = asset
        return stac
