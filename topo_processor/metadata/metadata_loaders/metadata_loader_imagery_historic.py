from __future__ import annotations

import csv
import numbers
import os
from typing import TYPE_CHECKING, Dict

import shapely.wkt
from linz_logger.logger import get_log
from rasterio.enums import ColorInterp

import topo_processor.stac.lds_cache as lds_cache
from topo_processor import stac
from topo_processor.file_system.get_fs import is_s3_path
from topo_processor.stac import lds_cache
from topo_processor.stac.asset_key import AssetKey
from topo_processor.stac.linz_provider import LinzProviders
from topo_processor.stac.providers import Providers
from topo_processor.stac.store import get_collection, get_item
from topo_processor.util import (
    h_i_photo_type_to_linz_geospatial_type,
    nzt_datetime_to_utc_datetime,
    quarterdate_to_date_string,
    remove_empty_strings,
    string_to_boolean,
    string_to_number,
)
from topo_processor.util.tiff import is_tiff

from .metadata_loader import MetadataLoader

if TYPE_CHECKING:
    from topo_processor.stac import Asset, Item


class MetadataLoaderImageryHistoric(MetadataLoader):
    name = "metadata.loader.imagery.historic"
    layer_id = "51002"
    is_init = False
    raw_metadata: Dict[str, Dict[str, str]] = {}

    def is_applicable(self, asset: Asset) -> bool:
        return is_tiff(asset.source_path)

    def load_metadata(self, asset: Asset) -> None:
        if not self.is_init:
            if not is_s3_path(asset.source_path):
                self.read_csv()
            else:
                metadata_file = lds_cache.get_layer(self.layer_id)
                self.read_csv(metadata_file)

        filename = os.path.splitext(os.path.basename(asset.source_path))[0]

        if filename not in self.raw_metadata:
            asset.add_error("Asset not found in CSV file", self.name)
            return
        asset_metadata = self.raw_metadata[filename]

        asset.target = f"{asset_metadata['survey']}/{asset_metadata['sufi']}{asset.file_ext()}"
        asset.key_name = AssetKey.Visual
        self.populate_item(asset_metadata, asset)

    def load_all_metadata(self, metadata_file: str) -> None:
        if not self.is_init:
            self.read_csv(metadata_file)

        for metadata in self.raw_metadata.values():
            self.populate_item(metadata)

    def populate_item(self, metadata_row, asset: Asset = None) -> None:
        title = self.get_title(metadata_row["survey"], metadata_row["alternate_survey_name"])
        if not title:
            get_log().warning(
                "Null collection title value", message="asset has null 'survey' and 'alternate_survey_name' values"
            )
            return
        collection = get_collection(title)

        item = get_item(metadata_row["sufi"])
        collection.add_item(item)

        if asset:
            item.add_asset(asset)

        item.collection = collection

        collection.license = "CC-BY-4.0"
        collection.description = "Historical Imagery"
        collection.extra_fields.update(
            {
                "linz:lifecycle": "completed",
                "linz:history": "LINZ and its predecessors, Lands & Survey and Department of Survey and Land Information (DOSLI), commissioned aerial photography for the Crown between 1936 and 2008.",
                "processing:software": {"Topo Processor": "0.1.0"},
                "version": "1",
            }
        )

        collection.add_extension(stac.StacExtensions.historical_imagery.value)
        collection.add_extension(stac.StacExtensions.linz.value)
        collection.add_extension(stac.StacExtensions.quality.value)
        collection.add_extension(stac.StacExtensions.processing.value)
        collection.add_extension(stac.StacExtensions.version.value)
        collection.add_linz_provider(LinzProviders.LTTW.value)
        collection.add_linz_provider(LinzProviders.LMPP.value)
        collection.add_provider(Providers.NZAM.value)

        item.properties.update(
            {
                "mission": title,
                "platform": "Fixed-wing Aircraft",
                "instruments": [metadata_row["camera"]],
                "processing:software": {"Topo Processor": "0.1.0"},
                "version": "1",
            }
        )

        self.add_linz_geospatial_type(item, metadata_row["photo_type"])
        self.add_centroid(item, metadata_row)
        self.add_camera_metadata(item, metadata_row)
        self.add_film_metadata(item, metadata_row)
        self.add_aerial_photo_metadata(item, metadata_row)
        self.add_scanning_metadata(item, metadata_row)
        self.add_datetime_property(item, metadata_row)
        self.add_spatial_extent(item, metadata_row)
        self.add_projection_extent(item)
        self.add_bands_extent(item, asset)

        item.add_extension(stac.StacExtensions.historical_imagery.value)
        item.add_extension(stac.StacExtensions.linz.value)
        item.add_extension(stac.StacExtensions.version.value)
        item.add_extension(stac.StacExtensions.processing.value)

    def read_csv(self, metadata_file: str = "") -> None:
        self.raw_metadata = {}
        if not metadata_file:
            metadata_file = "test_data/historical_aerial_photos_metadata.csv"

        csv_path = os.path.join(os.getcwd(), metadata_file)
        if not os.path.isfile(csv_path):
            raise Exception(f'Cannot find "{csv_path}"')

        with open(csv_path, "r") as csv_path:
            reader = csv.DictReader(csv_path, delimiter=",")
            for row in reader:
                if row["raw_filename"]:
                    raw_filename = row["raw_filename"]
                    if not metadata_file and raw_filename in self.raw_metadata:
                        raise Exception(f'Duplicate file "{raw_filename}" found in metadata csv')
                    self.raw_metadata[raw_filename] = row
                else:
                    self.raw_metadata[row["sufi"]] = row

        self.is_init = True

    def get_title(self, survey: str, alternate_survey_name: str):
        if not survey or survey == "0" or survey == "":
            if alternate_survey_name and alternate_survey_name != "":
                return alternate_survey_name
        else:
            return survey

    def add_spatial_extent(self, item: Item, asset_metadata: Dict[str, str]):
        wkt = asset_metadata.get("WKT", None)
        if wkt is None or wkt.lower() == "polygon empty":
            item.add_warning("Geometry is missing", "")
            return

        try:
            # EPSG:4167 -> EPSG:4326 is mostly a null conversion, in the future if we support additional projections we should reproject this
            poly = shapely.wkt.loads(wkt)
            # Reduce the precision of all the coordinates to approx 1M resolution
            poly = shapely.wkt.loads(shapely.wkt.dumps(poly, rounding_precision=5))
            item.geometry_poly = poly
        except shapely.errors.WKTReadingError as e:
            item.add_error("Geometry is invalid", "", e)

    def add_camera_metadata(self, item: Item, asset_metadata: Dict[str, str]):
        camera_properties = {}

        camera_properties["camera:sequence_number"] = string_to_number(asset_metadata["camera_sequence_no"])
        camera_properties["camera:nominal_focal_length"] = string_to_number(asset_metadata["nominal_focal_length"])

        item.properties.update(remove_empty_strings(camera_properties))
        item.add_extension(stac.StacExtensions.camera.value)

    def add_film_metadata(self, item: Item, asset_metadata: Dict[str, str]):
        film_properties = {}

        film_properties["film:id"] = asset_metadata["film"]
        film_properties["film:negative_sequence"] = string_to_number(asset_metadata["film_sequence_no"])
        film_properties["film:physical_condition"] = asset_metadata["physical_film_condition"]
        film_properties["film:physical_size"] = asset_metadata["format"]

        item.properties.update(remove_empty_strings(film_properties))
        item.add_extension(stac.StacExtensions.film.value)

    def add_aerial_photo_metadata(self, item: Item, asset_metadata: Dict[str, str]):
        aerial_photo_properties = {}
        aerial_photo_properties["aerial-photo:run"] = asset_metadata["run"]
        aerial_photo_properties["aerial-photo:sequence_number"] = string_to_number(asset_metadata["photo_no"])
        aerial_photo_properties["aerial-photo:anomalies"] = asset_metadata["image_anomalies"]
        altitude = string_to_number(asset_metadata["altitude"])
        if isinstance(altitude, int) and altitude <= 0:
            item.add_warning(
                msg="Skipped Record",
                cause=self.name,
                e=Exception(f"stac field 'aerial-photo:altitude' has value: {altitude}"),
            )
        else:
            aerial_photo_properties["aerial-photo:altitude"] = altitude
        scale = string_to_number(asset_metadata["scale"])
        if isinstance(scale, int) and scale <= 0:
            item.add_warning(
                msg="Skipped Record",
                cause=self.name,
                e=Exception(f"stac field 'aerial-photo:scale' has value: {scale}"),
            )
        else:
            aerial_photo_properties["aerial-photo:scale"] = scale

        item.properties.update(remove_empty_strings(aerial_photo_properties))
        item.add_extension(stac.StacExtensions.aerial_photo.value)

    def add_scanning_metadata(self, item: Item, asset_metadata: Dict[str, str]):
        scanning_properties = {}

        if asset_metadata["source"]:
            scanning_properties["scan:is_original"] = string_to_boolean(asset_metadata["source"], ["original"], ["copy"])
        if asset_metadata["when_scanned"]:
            scanning_properties["scan:scanned"] = quarterdate_to_date_string(asset_metadata["when_scanned"])

        item.properties.update(remove_empty_strings(scanning_properties))
        item.add_extension(stac.StacExtensions.scanning.value)

    def add_datetime_property(self, item: Item, asset_metadata: Dict[str, str]):
        item_date = asset_metadata.get("date", None)

        if item_date:
            try:
                item.datetime = nzt_datetime_to_utc_datetime(item_date)
            except Exception as e:
                item.add_error(msg="Invalid date", cause=self.name, e=e)
        else:
            item.add_error(msg="No date found", cause=self.name, e=Exception(f"item date has no value"))

    def add_centroid(self, item: Item, asset_metadata: Dict[str, str]):

        centroid = {
            "lat": string_to_number(asset_metadata.get("photocentre_lat", None)),
            "lon": string_to_number(asset_metadata.get("photocentre_lon", None)),
        }
        if self.is_valid_centroid(item, centroid):
            item.properties["proj:centroid"] = centroid
            item.add_extension(stac.StacExtensions.projection.value)

    def add_projection_extent(self, item: Item):
        item.properties["proj:epsg"] = None
        item.add_extension(stac.stac_extensions.StacExtensions.projection.value)

    def add_bands_extent(self, item: Item, asset: Asset):
        item.add_extension(stac.StacExtensions.eo.value)

        if asset:
            # default value
            asset.properties["eo:bands"] = [{"name": ColorInterp.gray.name, "common_name": "pan"}]

    def is_valid_centroid(self, item: Item, centroid) -> bool:
        if not isinstance(centroid["lat"], numbers.Number) or centroid["lat"] > 90 or centroid["lat"] < -90:
            item.add_warning(
                msg="Skipped Record",
                cause=self.name,
                e=Exception(
                    f"stac field 'proj:centroid' has invalid lat value: {centroid['lat']}, instance: {type(centroid['lat'])}"
                ),
            )
            return False
        if not isinstance(centroid["lon"], numbers.Number) or centroid["lon"] > 180 or centroid["lon"] < -180:
            item.add_warning(
                msg="Skipped Record",
                cause=self.name,
                e=Exception(
                    f"stac field 'proj:centroid' has invalid lon value: {centroid['lon']}, instance: {type(centroid['lat'])}"
                ),
            )
            return False
        return True

    def add_linz_geospatial_type(self, item: Item, photo_type) -> None:
        linz_geospatial_type_properties = {}
        linz_geospatial_type_properties["linz:geospatial_type"] = h_i_photo_type_to_linz_geospatial_type(photo_type)
        item.properties.update(linz_geospatial_type_properties)
