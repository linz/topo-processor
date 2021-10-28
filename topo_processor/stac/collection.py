from __future__ import annotations

import os
from datetime import datetime
from shutil import rmtree
from tempfile import mkdtemp
from typing import TYPE_CHECKING, Dict, List

import pystac
import ulid
from linz_logger import get_log
from shapely.ops import unary_union

from topo_processor.util import Validity

GLOBAL_PROVIDERS = [pystac.Provider(name="LINZ", description="Land Information New Zealand", roles=["host"])]
if TYPE_CHECKING:
    from .item import Item

TEMP_DIR = None


class Collection(Validity):
    title: str
    description: str
    license: str
    items: Dict[str, "Item"]
    providers: List[pystac.Provider]

    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.items = {}

    def add_item(self, item: Item):
        if item.collection is not None and item.collection != self:
            raise Exception(f"Remapping of collection? existing='{item.collection.title}' new='{self.title}' item='{item.id}'")
        if item.id in self.items:
            existing = self.items[item.id]
            if existing != item:
                raise Exception(f"Remapping of item id in collection='{self.title}' item='{item.id}'")
            return
        self.items[item.id] = item

    def get_temp_dir(self):
        global TEMP_DIR
        if not TEMP_DIR:
            TEMP_DIR = mkdtemp()
            get_log().debug("Temp directory created", path=TEMP_DIR)
        temp_dir = os.path.join(TEMP_DIR, self.title)
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        return temp_dir

    def get_temporal_extent(self) -> List[datetime | None]:
        min_date = None
        max_date = None

        for item in self.items.values():
            if item.datetime:
                if not min_date:
                    min_date = item.datetime
                elif item.datetime < min_date:
                    min_date = item.datetime

                if not max_date:
                    max_date = item.datetime
                elif item.datetime > max_date:
                    max_date = item.datetime

        return [min_date, max_date]

    def get_bounding_boxes(self):
        """
        create a union of all item bounding boxes inside the collection
        """
        polys = [x.geometry_poly for x in self.items.values() if x.geometry_poly is not None]

        if len(polys) == 0:
            return [(0.0, 0.0, 0.0, 0.0)]
        union_poly = unary_union(polys)
        return [union_poly.bounds]

    def delete_temp_dir(self):
        global TEMP_DIR
        if TEMP_DIR:
            if os.path.exists(TEMP_DIR):
                rmtree(TEMP_DIR)
                TEMP_DIR = None

    def create_stac(self) -> pystac.Collection:
        stac = pystac.Collection(
            id=str(ulid.ULID()),
            description=self.description,
            href="./collection.json",
            license=self.license,
            providers=GLOBAL_PROVIDERS,
            extent=pystac.Extent(
                pystac.SpatialExtent(bboxes=self.get_bounding_boxes()),
                pystac.TemporalExtent(intervals=[self.get_temporal_extent()]),
            ),
        )
        return stac
