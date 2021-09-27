import csv
import os
from typing import Dict

from topo_processor.stac import Asset, Item
from topo_processor.stac.stac_extensions import StacExtensions
from topo_processor.stac.store import get_collection, get_item

from .metadata_loader import MetadataLoader


class MetadataLoaderImageryHistoric(MetadataLoader):
    name = "metadata.loader.imagery.historic"
    is_init = False
    raw_metadata: Dict[str, Dict[str, str]] = {}

    def is_applicable(self, asset: Asset) -> bool:
        return True

    async def load_metadata(self, asset: Asset) -> None:
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
                "linz:run": asset_metadata["run"],
                "linz:photo_no": asset_metadata["photo_no"],
                "linz:alternate_survey_name": asset_metadata["alternate_survey_name"],
                "linz:camera": asset_metadata["camera"],
                "linz:altitude": asset_metadata["altitude"],
                "linz:scale": asset_metadata["scale"],
                "linz:photocentre_lat": asset_metadata["photocentre_lat"],
                "linz:photocentre_lon": asset_metadata["photocentre_lon"],
                "linz:date": asset_metadata["date"],
                "linz:film": asset_metadata["film"],
                "linz:film_sequence_no": asset_metadata["film_sequence_no"],
                "linz:photo_type": asset_metadata["photo_type"],
                "linz:format": asset_metadata["format"],
                "linz:source": asset_metadata["source"],
                "linz:physical_film_condition": asset_metadata["physical_film_condition"],
                "linz:image_anomalies": asset_metadata["image_anomalies"],
                "linz:scanned": asset_metadata["scanned"],
                "linz:raw_filename": asset_metadata["raw_filename"],
                "linz:released_filename": asset_metadata["released_filename"],
                "linz:when_scanned": asset_metadata["when_scanned"],
                "linz:photo_version": asset_metadata["photo_version"],
            }
        )
        self.add_camera_metadata(item, asset_metadata)

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
        try:
            camera_properties["camera:sequence_number"] = int(asset_metadata["camera_sequence_no"])
            camera_properties["camera:nominal_focal_length"] = int(asset_metadata["nominal_focal_length"])
        except ValueError as e:
            item.add_error(str(e), self.name, e)
            raise Exception(f"Invalid Camera Metadata: {e}")
        filtered_camera_properties = {field: value for field, value in camera_properties.items() if value}
        if len(filtered_camera_properties) > 0:
            item.properties.update(filtered_camera_properties)
            item.add_extension(StacExtensions.camera.value)
