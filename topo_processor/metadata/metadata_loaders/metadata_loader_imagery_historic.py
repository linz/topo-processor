import csv
import os
from typing import Dict

from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item
from topo_processor.util import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderImageryHistoric(MetadataLoader):
    name = "loader.imagery.historic"
    is_init = False
    raw_metadata: Dict[str, Dict[str, str]] = {}

    def is_applicable(self, item: Item) -> bool:
        if item.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.source_path):
            return False
        return True

    async def add_metadata(self, item: Item) -> None:
        if not self.is_init:
            self.read_csv()

        item.source_path_basename = os.path.splitext(os.path.basename(item.source_path))[0]
        if item.source_path_basename not in self.raw_metadata:
            raise Exception(f"{item.source_path_basename} cannot be found in the csv.")
        item_metadata = self.raw_metadata[item.source_path_basename]
        properties = {
            "linz:sufi": item_metadata["sufi"],
            "linz:survey": item_metadata["survey"],
            "linz:run": item_metadata["run"],
            "linz:photo_no": item_metadata["photo_no"],
            "linz:alternate_survey_name": item_metadata["alternate_survey_name"],
            "linz:camera": item_metadata["camera"],
            "linz:camera_sequence_no": item_metadata["camera_sequence_no"],
            "linz:nominal_focal_length": item_metadata["nominal_focal_length"],
            "linz:altitude": item_metadata["altitude"],
            "linz:scale": item_metadata["scale"],
            "linz:photocentre_lat": item_metadata["photocentre_lat"],
            "linz:photocentre_lon": item_metadata["photocentre_lon"],
            "linz:date": item_metadata["date"],
            "linz:film": item_metadata["film"],
            "linz:film_sequence_no": item_metadata["film_sequence_no"],
            "linz:photo_type": item_metadata["photo_type"],
            "linz:format": item_metadata["format"],
            "linz:source": item_metadata["source"],
            "linz:physical_film_condition": item_metadata["physical_film_condition"],
            "linz:image_anomalies": item_metadata["image_anomalies"],
            "linz:scanned": item_metadata["scanned"],
            "linz:raw_filename": item_metadata["raw_filename"],
            "linz:released_filename": item_metadata["released_filename"],
            "linz:when_scanned": item_metadata["when_scanned"],
            "linz:photo_version": item_metadata["photo_version"],
        }
        item.properties.update(properties)
        item.id = item_metadata["sufi"]
        item.metadata_path = f"{item_metadata['survey']}/{item_metadata['sufi']}.json"

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
