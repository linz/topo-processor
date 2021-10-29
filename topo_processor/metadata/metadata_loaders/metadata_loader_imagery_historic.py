from __future__ import annotations

import csv
import os
from typing import TYPE_CHECKING, Dict

import shapely.wkt

from topo_processor import stac
from topo_processor.stac.store import get_collection, get_item
from topo_processor.util import quarterdate_to_datetime, remove_empty_strings, string_to_boolean, string_to_number

from .metadata_loader import MetadataLoader

if TYPE_CHECKING:
    from topo_processor.stac import Asset, Item


class MetadataLoaderImageryHistoric(MetadataLoader):
    name = "metadata.loader.imagery.historic"
    is_init = False
    raw_metadata: Dict[str, Dict[str, str]] = {}

    def is_applicable(self, asset: Asset) -> bool:
        return True

    def load_metadata(self, asset: Asset) -> None:
        if not self.is_init:
            self.read_csv()

        filename = os.path.splitext(os.path.basename(asset.source_path))[0]

        if filename not in self.raw_metadata:
            asset.add_error("Asset not found in CSV file", self.name)
            return
        asset_metadata = self.raw_metadata[filename]

        asset.target = f"{asset_metadata['survey']}/{asset_metadata['sufi']}{asset.file_ext()}"

        self.populate_item(asset_metadata, asset)

    def load_all_metadata(self, metadata_file: str) -> None:
        if not self.is_init:
            self.read_csv(metadata_file)

        for metadata in self.raw_metadata.values():
            self.populate_item(metadata)

    def populate_item(self, metadata_row, asset: Asset = None) -> None:
        collection = get_collection(metadata_row["survey"])
        item = get_item(metadata_row["sufi"])
        collection.add_item(item)

        if asset:
            item.add_asset(asset)

        item.collection = collection

        collection.license = "CC-BY-4.0"
        collection.description = "Historical Imagery"

        item.properties.update(
            {
                "linz:sufi": metadata_row["sufi"],
                "linz:survey": metadata_row["survey"],
                "linz:alternate_survey_name": metadata_row["alternate_survey_name"],
                "linz:camera": metadata_row["camera"],
                "linz:photocentre_lat": metadata_row["photocentre_lat"],
                "linz:photocentre_lon": metadata_row["photocentre_lon"],
                "linz:date": metadata_row["date"],
                "linz:photo_type": metadata_row["photo_type"],
                "linz:scanned": metadata_row["scanned"],
                "linz:raw_filename": metadata_row["raw_filename"],
                "linz:released_filename": metadata_row["released_filename"],
                "linz:photo_version": metadata_row["photo_version"],
            }
        )
        self.add_camera_metadata(item, metadata_row)
        self.add_film_metadata(item, metadata_row)
        self.add_aerial_photo_metadata(item, metadata_row)
        self.add_scanning_metadata(item, metadata_row)
        self.add_spatial_extent(item, metadata_row)

    def read_csv(self, metadata_file: str = "") -> None:
        self.raw_metadata = {}
        if not metadata_file:
            metadata_file = "historical_aerial_photos_metadata.csv"

        csv_path = os.path.join(os.getcwd(), "test_data", metadata_file)
        if not os.path.isfile(csv_path):
            raise Exception(f'Cannot find "{csv_path}"')

        with open(csv_path, "r") as csv_path:
            reader = csv.DictReader(csv_path, delimiter=",")
            for row in reader:
                if row["released_filename"]:
                    released_filename = row["released_filename"]
                    if not metadata_file and released_filename in self.raw_metadata:
                        raise Exception(f'Duplicate file "{released_filename}" found in metadata csv')
                    self.raw_metadata[released_filename] = row
                else:
                    self.raw_metadata[row["sufi"]] = row

        self.is_init = True

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
            scanning_properties["scan:scanned"] = quarterdate_to_datetime(asset_metadata["when_scanned"])

        item.properties.update(remove_empty_strings(scanning_properties))
        item.add_extension(stac.StacExtensions.scanning.value)
