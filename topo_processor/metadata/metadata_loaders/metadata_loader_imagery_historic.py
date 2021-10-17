from __future__ import annotations

import csv
import os
from typing import TYPE_CHECKING, Dict

import topo_processor.stac as stac
from topo_processor.stac.store import get_collection, get_item
from topo_processor.util import copy_or_original, quarterdate_to_datetime, remove_empty_strings, string_to_number

from .metadata_loader import MetadataLoader

if TYPE_CHECKING:
    from topo_processor.stac import Asset, Item

from linz_logger import get_log


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

        collection = get_collection(asset_metadata["survey"])
        item = get_item(asset_metadata["sufi"])
        collection.add_item(item)
        item.add_asset(asset)
        item.collection = collection

        collection.license = "CC-BY-4.0"
        collection.description = "Historical Imagery"

        item.properties.update(
            {
                "linz:sufi": asset_metadata["sufi"],
                "linz:survey": asset_metadata["survey"],
                "linz:alternate_survey_name": asset_metadata["alternate_survey_name"],
                "linz:camera": asset_metadata["camera"],
                "linz:photocentre_lat": asset_metadata["photocentre_lat"],
                "linz:photocentre_lon": asset_metadata["photocentre_lon"],
                "linz:date": asset_metadata["date"],
                "linz:photo_type": asset_metadata["photo_type"],
                "linz:scanned": asset_metadata["scanned"],
                "linz:raw_filename": asset_metadata["raw_filename"],
                "linz:released_filename": asset_metadata["released_filename"],
                "linz:photo_version": asset_metadata["photo_version"],
            }
        )
        self.add_camera_metadata(item, asset_metadata)
        self.add_film_metadata(item, asset_metadata)
        self.add_aerial_photo_metadata(item, asset_metadata)
        self.add_scanning_metadata(item, asset_metadata)

    def read_csv(self):
        self.raw_metadata = {}
        csv_path = os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata.csv")
        if not os.path.isfile(csv_path):
            raise Exception('Missing "historical_aerial_photos_metadata.csv"')

        with open(csv_path, "r") as csv_path:
            reader = csv.DictReader(csv_path, delimiter=",")
            for row in reader:
                released_filename = row["released_filename"]
                if released_filename in self.raw_metadata:
                    raise Exception(f'Duplicate file "{released_filename}" found in metadata csv')
                self.raw_metadata[released_filename] = row

        self.is_init = True

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
            scanning_properties["scan:is_original"] = copy_or_original(asset_metadata["source"], ["original"], ["copy"])
        if asset_metadata["when_scanned"]:
            scanning_properties["scan:scanned"] = quarterdate_to_datetime(asset_metadata["when_scanned"])

        item.properties.update(remove_empty_strings(scanning_properties))
        item.add_extension(stac.StacExtensions.scanning.value)
