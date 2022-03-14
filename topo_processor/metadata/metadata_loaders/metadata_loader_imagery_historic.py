from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import shapely.wkt
from linz_logger.logger import get_log
from rasterio.enums import ColorInterp

from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.lds_cache.lds_cache import get_metadata
from topo_processor.stac.asset_key import AssetKey
from topo_processor.stac.linz_provider import LinzProviders
from topo_processor.stac.providers import Providers
from topo_processor.stac.stac_extensions import StacExtensions
from topo_processor.stac.store import get_collection, get_item
from topo_processor.util.conversions import (
    historical_imagery_photo_type_to_linz_geospatial_type,
    nzt_datetime_to_utc_datetime,
    quarterdate_to_date_string,
    remove_empty_strings,
    string_to_boolean,
    string_to_number,
)
from topo_processor.util.file_extension import is_tiff

from .metadata_loader import MetadataLoader

if TYPE_CHECKING:
    from topo_processor.stac.asset import Asset
    from topo_processor.stac.item import Item


class MetadataLoaderImageryHistoric(MetadataLoader):
    name = "metadata.loader.imagery.historic"
    is_init = False
    raw_metadata: Dict[str, Dict[str, str]] = {}

    def is_applicable(self, asset: Optional[Asset] = None) -> bool:
        if asset:
            return is_tiff(asset.source_path)
        else:
            return False

    def load_metadata(self, asset: Optional[Asset] = None, metadata_file: str = "", is_load_all: bool = False) -> None:
        criteria = {}
        filename = ""

        if asset:
            filename = os.path.splitext(os.path.basename(asset.source_path))[0]
            criteria = {"raw_filename": filename}

        self.raw_metadata = get_metadata(DataType.IMAGERY_HISTORIC.value, criteria, metadata_file)

        if is_load_all:
            for metadata in self.raw_metadata.values():
                self.populate_item(metadata)
        elif asset:

            if filename not in self.raw_metadata:
                asset.add_error("Asset not found in CSV file", self.name)
                return
            asset_metadata = self.raw_metadata[filename]

            asset.target = f"{asset_metadata['survey']}/{asset_metadata['sufi']}{asset.file_ext()}"
            asset.key_name = AssetKey.Visual
            self.populate_item(asset_metadata, asset)


    def populate_item(self, metadata_row: Dict[str, str], asset: Optional[Asset] = None) -> None:
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
                "linz:history": "LINZ and its predecessors, Lands & Survey and Department of Survey and Land Information (DOSLI), commissioned aerial photography for the Crown between 1936 and 2008.\nOne of the predominant uses of the aerial photography at the time was the photogrammetric mapping of New Zealand, initially at 1inch to 1mile followed by the NZMS 260 and Topo50 map series at 1:50,000.\nThese photographs were scanned through the Crown Aerial Film Archive scanning project.",
            }
        )

        collection.add_extension(StacExtensions.quality.value)

        collection.add_linz_provider(LinzProviders.LTTW.value)
        collection.add_linz_provider(LinzProviders.LMPP.value)
        collection.add_provider(Providers.NZAM.value)

        item.properties.update(
            {
                "mission": title,
                "platform": "Fixed-wing Aircraft",
                "instruments": [metadata_row["camera"]],
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

        item.add_extension(StacExtensions.historical_imagery.value)
        item.add_extension(StacExtensions.linz.value)
        item.add_extension(StacExtensions.version.value)
        item.add_extension(StacExtensions.processing.value)

    def get_title(self, survey: str, alternate_survey_name: str) -> Union[str, None]:
        if not survey or survey == "0" or survey == "":
            if alternate_survey_name and alternate_survey_name != "":
                return alternate_survey_name
            else:
                return None
        else:
            return survey

    def add_spatial_extent(self, item: Item, asset_metadata: Dict[str, str]) -> None:
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

    def add_camera_metadata(self, item: Item, asset_metadata: Dict[str, str]) -> None:
        camera_properties: Dict[str, Any] = {}

        camera_properties["camera:sequence_number"] = string_to_number(asset_metadata["camera_sequence_no"])
        camera_properties["camera:nominal_focal_length"] = string_to_number(asset_metadata["nominal_focal_length"])

        item.properties.update(remove_empty_strings(camera_properties))
        item.add_extension(StacExtensions.camera.value)

    def add_film_metadata(self, item: Item, asset_metadata: Dict[str, str]) -> None:
        film_properties: Dict[str, Any] = {}

        film_properties["film:id"] = asset_metadata["film"]
        film_properties["film:negative_sequence"] = string_to_number(asset_metadata["film_sequence_no"])
        film_properties["film:physical_condition"] = asset_metadata["physical_film_condition"]
        film_properties["film:physical_size"] = asset_metadata["format"]

        item.properties.update(remove_empty_strings(film_properties))
        item.add_extension(StacExtensions.film.value)

    def add_aerial_photo_metadata(self, item: Item, asset_metadata: Dict[str, str]) -> None:
        aerial_photo_properties: Dict[str, Any] = {}
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
        item.add_extension(StacExtensions.aerial_photo.value)

    def add_scanning_metadata(self, item: Item, asset_metadata: Dict[str, str]) -> None:
        scanning_properties: Dict[str, Any] = {}

        if asset_metadata["source"]:
            scanning_properties["scan:is_original"] = string_to_boolean(asset_metadata["source"], ["original"], ["copy"])
        if asset_metadata["when_scanned"]:
            scanning_properties["scan:scanned"] = quarterdate_to_date_string(asset_metadata["when_scanned"])

        item.properties.update(remove_empty_strings(scanning_properties))
        item.add_extension(StacExtensions.scanning.value)

    def add_datetime_property(self, item: Item, asset_metadata: Dict[str, str]) -> None:
        item_date = asset_metadata.get("date", None)

        if item_date:
            try:
                item.datetime = nzt_datetime_to_utc_datetime(item_date)
            except Exception as e:
                item.add_error(msg="Invalid date", cause=self.name, e=e)
        else:
            item.add_error(msg="No date found", cause=self.name, e=Exception(f"item date has no value"))

    def add_centroid(self, item: Item, asset_metadata: Dict[str, str]) -> None:

        centroid = {
            "lat": string_to_number(asset_metadata.get("photocentre_lat", "")),
            "lon": string_to_number(asset_metadata.get("photocentre_lon", "")),
        }
        if self.is_valid_centroid(item, centroid):
            item.properties["proj:centroid"] = centroid
            item.add_extension(StacExtensions.projection.value)

    def add_projection_extent(self, item: Item) -> None:
        item.properties["proj:epsg"] = None
        item.add_extension(StacExtensions.projection.value)

    def add_bands_extent(self, item: Item, asset: Optional[Asset] = None) -> None:
        item.add_extension(StacExtensions.eo.value)

        if asset:
            # default value
            asset.properties["eo:bands"] = [{"name": ColorInterp.gray.name, "common_name": "pan"}]

    def is_valid_centroid(self, item: Item, centroid: Dict[str, Any]) -> bool:
        if not isinstance(centroid["lat"], (int, float)) or centroid["lat"] > 90 or centroid["lat"] < -90:
            item.add_warning(
                msg="Skipped Record",
                cause=self.name,
                e=Exception(
                    f"stac field 'proj:centroid' has invalid lat value: {centroid['lat']}, instance: {type(centroid['lat'])}"
                ),
            )
            return False
        if not isinstance(centroid["lon"], (int, float)) or centroid["lon"] > 180 or centroid["lon"] < -180:
            item.add_warning(
                msg="Skipped Record",
                cause=self.name,
                e=Exception(
                    f"stac field 'proj:centroid' has invalid lon value: {centroid['lon']}, instance: {type(centroid['lon'])}"
                ),
            )
            return False
        return True

    def add_linz_geospatial_type(self, item: Item, photo_type: str) -> None:

        item.linz_geospatial_type = historical_imagery_photo_type_to_linz_geospatial_type(photo_type)
