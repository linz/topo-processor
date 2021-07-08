import os
from shutil import rmtree
from tempfile import mkdtemp
from typing import TYPE_CHECKING, Dict, List

import pystac
import ulid
from linz_logger import get_log

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

    def add_item(self, item: "Item"):
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
            license=self.license,
            providers=GLOBAL_PROVIDERS,
            extent=pystac.Extent(pystac.SpatialExtent(bboxes=[0, 0, 0, 0]), pystac.TemporalExtent(intervals=[None, None])),
        )
        return stac
