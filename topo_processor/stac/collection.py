from __future__ import annotations

import os
from datetime import datetime
from shutil import rmtree
from tempfile import mkdtemp
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set

import pystac
import ulid
from linz_logger import get_log
from pystac.summaries import Summaries, Summarizer
from pystac.validation.schema_uri_map import DefaultSchemaUriMap
from shapely.ops import unary_union

from topo_processor.metadata.data_type import DataType
from topo_processor.stac.asset import Asset
from topo_processor.util.time import get_min_max_interval
from topo_processor.util.valid import Validity

from .linz_provider import LinzProvider
from .providers import Providers
from .stac_extensions import StacExtensions

if TYPE_CHECKING:
    from .item import Item

TEMP_DIR: Optional[str] = None
FIELDS_JSON_URL = "https://raw.githubusercontent.com/linz/stac/master/fields/fields.json"


class Collection(Validity):
    id: str
    title: str
    survey: str
    description: str
    license: str
    items: Dict[str, "Item"]
    linz_providers: List[Dict[str, Any]]
    providers: List[pystac.Provider]
    schema: Optional[str]
    extra_fields: Dict[str, Any]
    linz_geospatial_type: str

    stac_extensions: Set[str]
    summaries: Summaries = Summaries.empty()

    def __init__(self, title: str):
        super().__init__()
        # FIXME: Do we want to generate this id like this?
        self.id = str(ulid.ULID())
        self.title = title
        self.description = ""
        self.items = {}
        self.schema = DefaultSchemaUriMap().get_object_schema_uri(pystac.STACObjectType.COLLECTION, pystac.get_stac_version())
        self.extra_fields = dict(
            {
                # TODO: decision to be made on version ref comments [TDE-230] hardcode to '1' for now
                "version": "1",
                "linz:security_classification": "unclassified",
            }
        )
        self.linz_providers = []
        self.stac_extensions = set([StacExtensions.file.value])
        self.providers = [Providers.TTW.value]

    def add_item(self, item: Item) -> None:
        if item.collection is not None and item.collection != self:
            raise Exception(f"Remapping of collection? existing='{item.collection.title}' new='{self.title}' item='{item.id}'")
        if item.id in self.items:
            existing = self.items[item.id]
            if existing != item:
                raise Exception(f"Remapping of item id in collection='{self.title}' item='{item.id}'")
            return
        self.items[item.id] = item

    def add_extension(self, ext: str) -> None:
        self.stac_extensions.add(ext)

    def add_provider(self, provider: pystac.Provider) -> None:
        if provider not in self.providers:
            self.providers.append(provider)

    def add_linz_provider(self, linz_provider: LinzProvider) -> None:
        if linz_provider.to_dict() not in self.linz_providers:
            self.linz_providers.append(linz_provider.to_dict())

    def update_description(self, stac_collection: pystac.Collection, data_type: DataType) -> None:
        if data_type == DataType.IMAGERY_HISTORIC:
            size = self.summaries.to_dict()["film:physical_size"]
            if len(size) == 1:
                size = size[0]
            colour = self.extra_fields["linz:geospatial_type"]
            stac_collection.description = (
                self.description
            ) = f"This aerial photographic survey was digitised from {colour} {size} negatives in the Crown collection of the Crown Aerial Film Archive."

    def get_temp_dir(self) -> str:
        global TEMP_DIR
        if not TEMP_DIR:
            TEMP_DIR = mkdtemp()
            get_log().debug("Temp directory created", path=TEMP_DIR)
        temp_dir = os.path.join(TEMP_DIR, self.title)
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        return temp_dir

    def get_temporal_extent(self) -> List[Optional[datetime]]:
        dates: List[datetime] = []

        for item in self.items.values():
            if item.datetime:
                dates.append(item.datetime)

        return get_min_max_interval(dates)

    def get_bounding_boxes(self) -> List[List[float]]:
        """
        create a union of all item bounding boxes inside the collection
        """
        polys = [x.geometry_poly for x in self.items.values() if x.geometry_poly is not None]

        if len(polys) == 0:
            return [[0.0, 0.0, 0.0, 0.0]]
        union_poly = unary_union(polys)
        return [list(union_poly.bounds)]

    def get_linz_geospatial_type(self) -> str:
        geospatial_type_set = set(x.linz_geospatial_type for x in self.items.values() if x.linz_geospatial_type)
        if len(geospatial_type_set) != 1:
            get_log().warning(f"Invalid 'linz:geospatial_type' collection='{self.title}'")
            return "invalid geospatial type"
        geospatial_type_str = geospatial_type_set.pop()
        return geospatial_type_str

    def get_linz_asset_summaries(self) -> Dict[str, Any]:
        assets_checked: List[Asset] = []
        dates_created: List[datetime] = []
        dates_updated: List[datetime] = []
        processing_software_versions: List[Dict[str, str]] = []

        for item in self.items.values():
            for asset in item.assets:
                if not asset.needs_upload:
                    continue
                if not asset in assets_checked:
                    if "created" in asset.properties:
                        dates_created.append(asset.properties["created"])
                        dates_updated.append(asset.properties["updated"])
                    if "processing:software" in asset.properties:
                        if asset.properties["processing:software"] not in processing_software_versions:
                            processing_software_versions.append(asset.properties["processing:software"])
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
            "processing:software": processing_software_versions,
            "created": {"minimum": interval_created[0], "maximum": interval_created[1]},
            "updated": {"minimum": interval_updated[0], "maximum": interval_updated[1]},
        }

    def delete_temp_dir(self) -> None:
        global TEMP_DIR
        if TEMP_DIR:
            if os.path.exists(TEMP_DIR):
                rmtree(TEMP_DIR)
                TEMP_DIR = None

    def generate_summaries(self, collection: pystac.Collection) -> None:
        summarizer = Summarizer(fields=FIELDS_JSON_URL)
        collection.summaries = summarizer.summarize(collection)
        self.summaries = collection.summaries

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
            stac_extensions=list(sorted(self.stac_extensions)),
            href="./collection.json",
            extra_fields=self.extra_fields,
            license=self.license,
            providers=self.providers,
        )
        get_log().info("Stac Collection Created", id=stac.id, title=stac.title)
        return stac
