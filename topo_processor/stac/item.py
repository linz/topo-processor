import datetime as dt
from typing import Any, Dict, List, Optional, Set

import shapely.geometry
from pystac import pystac
from pystac.validation.schema_uri_map import DefaultSchemaUriMap

from topo_processor.util import Validity

from .asset import Asset
from .collection import Collection
from .stac_extensions import StacExtensions


class Item(Validity):

    id: str
    geometry_poly: Optional[shapely.geometry.Polygon] = None
    linz_geospatial_type: str = ""
    datetime: Optional[dt.datetime] = None
    properties: Dict[str, Any]
    stac_extensions: Set[str]
    assets: List[Asset]
    collection: Optional[Collection] = None
    schema: Optional[str]

    def __init__(self, item_id: str):
        super().__init__()
        self.id = item_id
        self.properties = {
            # TODO: [TDE-237] to generate release versioning
            "processing:software": {"Topo Processor": "0.1.0"},
            # TODO: decision to be made on version ref comments [TDE-230] hardcode to '1' for now
            "version": "1",
        }
        self.stac_extensions = set([StacExtensions.file.value])
        self.assets = []
        self.schema = DefaultSchemaUriMap().get_object_schema_uri(pystac.STACObjectType.ITEM, pystac.get_stac_version())

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        for asset in self.assets:
            if not asset.is_valid():
                return False
        return True

    def add_asset(self, asset: Asset) -> None:
        if asset.item:
            raise Exception(f"Asset is already associated with an item: existing item='{asset.item.id}' new item='{self.id}'")
        self.assets.append(asset)
        asset.item = self

    def add_extension(self, ext: str, add_to_collection: bool = True) -> None:
        self.stac_extensions.add(ext)
        if not self.collection:
            return
        if add_to_collection:
            self.collection.add_extension(ext)

    def create_stac(self) -> pystac.Item:
        geometry = None
        bbox = None
        if self.geometry_poly is not None:
            geometry = shapely.geometry.mapping(self.geometry_poly)
            bbox = self.geometry_poly.bounds

        stac = pystac.Item(
            id=self.id,
            geometry=geometry,
            bbox=bbox,
            datetime=self.datetime,
            properties=self.properties,
            stac_extensions=list(self.stac_extensions),
        )
        return stac
