import datetime
from typing import List

import pystac

from topo_processor.util import Validity

from .asset import Asset
from .collection import Collection
from .stac_extensions import StacExtensions


class Item(Validity):

    id: str
    geometry: str
    bbox: str
    datetime: datetime.datetime
    properties: dict
    stac_extensions: set
    collection: Collection
    assets: List[Asset]

    def __init__(self, item_id: str):
        super().__init__()
        self.id = item_id
        self.datetime = datetime.datetime.now()
        self.properties = {}
        self.stac_extensions = set([StacExtensions.file.value])
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
            datetime=self.datetime,
            properties=self.properties,
            stac_extensions=list(self.stac_extensions),
        )
        return stac
