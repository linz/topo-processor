from datetime import datetime
from typing import List

import pystac

from topo_processor.util import Validity

from .asset import Asset
from .collection import Collection


class Item(Validity):

    id: str
    gemoetry: str
    bbox: str
    datetime: datetime
    properties: dict
    stac_extensions: set
    collection: Collection
    assets: List[Asset]

    def __init__(self, item_id: str):
        super().__init__()
        self.id = item_id
        self.properties = {}
        self.stac_extensions = set(["https://stac-extensions.github.io/file/v2.0.0/schema.json"])
        self.collection = None
        self.assets = []

    def is_valid(self):
        if not super().is_valid():
            return False
        for asset in self.assets:
            if not asset.is_valid():
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
