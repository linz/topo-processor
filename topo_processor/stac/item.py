from datetime import datetime as DateTime
from typing import List

import shapely.geometry
from pystac import get_stac_version
from pystac.item import Item as PystacItem
from pystac.stac_object import STACObjectType
from pystac.validation.schema_uri_map import DefaultSchemaUriMap

from topo_processor.util.valid import Validity

from .asset import Asset
from .collection import Collection
from .stac_extensions import StacExtensions


class Item(Validity):

    id: str
    geometry_poly: shapely.geometry.Polygon
    linz_geospatial_type: str
    datetime: DateTime
    properties: dict
    stac_extensions: set
    collection: Collection
    assets: List[Asset]
    schema: str

    def __init__(self, item_id: str):
        super().__init__()
        self.id = item_id
        self.datetime = None
        self.properties = {
            # TODO: [TDE-237] to generate release versioning
            "processing:software": {"Topo Processor": "0.1.0"},
            # TODO: decision to be made on version ref comments [TDE-230] hardcode to '1' for now
            "version": "1",
        }
        self.stac_extensions = set([StacExtensions.file.value])
        self.collection = None
        self.geometry_poly = None
        self.linz_geospatial_type = ""
        self.assets = []
        self.schema = DefaultSchemaUriMap().get_object_schema_uri(STACObjectType.ITEM, get_stac_version())

    def is_valid(self):
        if not super().is_valid():
            return False
        for asset in self.assets:
            if not asset.is_valid():
                return False
        return True

    def add_asset(self, asset: Asset):
        if asset.item:
            raise Exception(f"Asset is already associated with an item: existing item='{asset.item.id}' new item='{self.id}'")
        self.assets.append(asset)
        asset.item = self

    def add_extension(self, ext: str, add_to_collection: bool = True):
        self.stac_extensions.add(ext)
        if add_to_collection:
            self.collection.add_extension(ext)

    def create_stac(self) -> PystacItem:
        geometry = None
        bbox = None
        if self.geometry_poly is not None:
            geometry = shapely.geometry.mapping(self.geometry_poly)
            bbox = self.geometry_poly.bounds

        stac = PystacItem(
            id=self.id,
            geometry=geometry,
            bbox=bbox,
            datetime=self.datetime,
            properties=self.properties,
            stac_extensions=list(self.stac_extensions),
        )
        return stac
