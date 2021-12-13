from __future__ import annotations

import os
from datetime import datetime
from shutil import rmtree
from tempfile import mkdtemp
from typing import TYPE_CHECKING, Dict, List

import pystac
import ulid
from linz_logger import get_log
from pystac.summaries import Summaries, Summarizer
from pystac.validation.schema_uri_map import DefaultSchemaUriMap
from shapely.ops import unary_union

from topo_processor.stac.asset import Asset
from topo_processor.util import Validity
from topo_processor.util.time import get_min_max_interval

from .linz_provider import LinzProvider
from .providers import Providers
from .stac_extensions import StacExtensions

if TYPE_CHECKING:
    from .item import Item

TEMP_DIR = None
FIELDS_JSON_URL = "https://raw.githubusercontent.com/linz/stac/master/fields/fields.json"


class Collection(Validity):
    id: str
    title: str
    description: str
    license: str
    items: Dict[str, "Item"]
    linz_providers: List[LinzProvider]
    providers: List[pystac.Provider]
    schema: str
    extra_fields: Dict[str, Any]
    linz_geospatial_type: str

    stac_extensions: set
    summaries: Summaries

    def __init__(self, title: str):
        super().__init__()
        # FIXME: Do we want to generate this id like this?
        self.id = str(ulid.ULID())
        self.title = title
        self.items = {}
        self.schema = DefaultSchemaUriMap().get_object_schema_uri(pystac.STACObjectType.COLLECTION, pystac.get_stac_version())
        self.stac_extensions = set([])
        self.extra_fields = dict(
            {
                "linz:security_classification": "unclassified",
                # TODO: [TDE-237] to generate release versioning
                "processing:software": {"Topo Processor": "0.1.0"},
                # TODO: decision to be made on version ref comments [TDE-230] hardcode to '1' for now
                "version": "1",
            }
        )
        self.linz_providers = []
        self.stac_extensions = set([StacExtensions.file.value])
        self.providers = [Providers.TTW.value]
        self.summaries = Summaries.empty()

    def add_item(self, item: Item):
        if item.collection is not None and item.collection != self:
            raise Exception(f"Remapping of collection? existing='{item.collection.title}' new='{self.title}' item='{item.id}'")
        if item.id in self.items:
            existing = self.items[item.id]
            if existing != item:
                raise Exception(f"Remapping of item id in collection='{self.title}' item='{item.id}'")
            return
        self.items[item.id] = item

    def add_extension(self, ext: str):
        self.stac_extensions.add(ext)

    def add_provider(self, provider: pystac.Provider):
        if provider not in self.providers:
            self.providers.append(provider)

    def add_linz_provider(self, linz_provider: LinzProvider):
        if linz_provider.to_dict() not in self.linz_providers:
            self.linz_providers.append(linz_provider.to_dict())

    def get_temp_dir(self):
        global TEMP_DIR
        if not TEMP_DIR:
            TEMP_DIR = mkdtemp()
            get_log().debug("Temp directory created", path=TEMP_DIR)
        temp_dir = os.path.join(TEMP_DIR, self.title)
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        return temp_dir

    def get_temporal_extent(self) -> List[datetime]:
        dates: List[datetime] = []

        for item in self.items.values():
            if item.datetime:
                dates.append(item.datetime)

        return get_min_max_interval(dates)

    def get_bounding_boxes(self):
        """
        create a union of all item bounding boxes inside the collection
        """
        polys = [x.geometry_poly for x in self.items.values() if x.geometry_poly is not None]

        if len(polys) == 0:
            return [(0.0, 0.0, 0.0, 0.0)]
        union_poly = unary_union(polys)
        return [union_poly.bounds]

    def get_linz_geospatial_type(self) -> str:
        geospatial_type_set = set(x.linz_geospatial_type for x in self.items.values() if x.linz_geospatial_type)
        if len(geospatial_type_set) != 1:
            get_log().warning(f"Invalid 'linz:geospatial_type' collection='{self.title}'")
            return "invalid geospatial type"
        geospatial_type_str = geospatial_type_set.pop()
        return geospatial_type_str

    def get_linz_asset_summaries(self) -> Dict:
        assets_checked: List[Asset] = []
        dates_created: List[datetime] = []
        dates_updated: List[datetime] = []

        for item in self.items.values():
            for asset in item.assets:
                if not asset in assets_checked:
                    if "created" in asset.properties:
                        dates_created.append(asset.properties["created"])
                        dates_updated.append(asset.properties["updated"])
                    assets_checked.append(asset)

        interval_created = get_min_max_interval(dates_created)
        interval_updated = get_min_max_interval(dates_updated)

        # to pass metadata-only validation as there are no assets to populate mandatory linz:asset_summaries
        # TODO: review this workaround once validation command has been combined into upload command
        if not assets_checked:
            return {
                "created": {"minimum": "0000-01-01T00:00:00Z", "maximum": "0000-01-01T00:00:00Z"},
                "updated": {"minimum": "0000-01-01T00:00:00Z", "maximum": "0000-01-01T00:00:00Z"},
            }

        return {
            "created": {"minimum": interval_created[0], "maximum": interval_created[1]},
            "updated": {"minimum": interval_updated[0], "maximum": interval_updated[1]},
        }

    def delete_temp_dir(self):
        global TEMP_DIR
        if TEMP_DIR:
            if os.path.exists(TEMP_DIR):
                rmtree(TEMP_DIR)
                TEMP_DIR = None

    def generate_summaries(self, collection: pystac.Collection):
        summarizer = Summarizer(fields=FIELDS_JSON_URL)
        collection.summaries = summarizer.summarize(collection)

    def create_stac(self) -> pystac.Collection:
        if self.linz_providers:
            self.extra_fields["linz:providers"] = self.linz_providers
        self.extra_fields["linz:geospatial_type"] = self.get_linz_geospatial_type()
        self.extra_fields["linz:asset_summaries"] = self.get_linz_asset_summaries()
        stac = pystac.Collection(
            id=self.id,
            description=self.description,
            extent=pystac.Extent(
                pystac.SpatialExtent(bboxes=self.get_bounding_boxes()),
                pystac.TemporalExtent(intervals=[self.get_temporal_extent()]),
            ),
            title=self.title,
            stac_extensions=list(self.stac_extensions),
            href="./collection.json",
            license=self.license,
            extra_fields=self.extra_fields,
            providers=self.providers,
        )
        return stac
