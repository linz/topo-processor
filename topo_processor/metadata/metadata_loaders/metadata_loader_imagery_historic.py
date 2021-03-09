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
    csv_dict: Dict[str, Dict[str, str]] = {}

    def is_applicable(self, item: Item) -> bool:
        if item.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.source_file):
            return False
        return True

    async def add_metadata(self, item: Item) -> None:
        if not self.is_init:
            self.read_csv()

        source_file_basename = os.path.splitext(os.path.basename(item.source_file))[0]
        if source_file_basename not in self.csv_dict:
            raise Exception(f"{source_file_basename} cannot be found in the csv.")
        item_dict = self.csv_dict[source_file_basename]
        properties = {
            "linz:sufi": item_dict["sufi"],
            "linz:survey": item_dict["survey"],
            "linz:run": item_dict["run"],
            "linz:photo_no": item_dict["photo_no"],
            "linz:alternate_survey_name": item_dict["alternate_survey_name"],
            "linz:camera": item_dict["camera"],
            "linz:camera_sequence_no": item_dict["camera_sequence_no"],
            "linz:nominal_focal_length": item_dict["nominal_focal_length"],
            "linz:altitude": item_dict["altitude"],
            "linz:scale": item_dict["scale"],
            "linz:photocentre_lat": item_dict["photocentre_lat"],
            "linz:photocentre_lon": item_dict["photocentre_lon"],
            "linz:date": item_dict["date"],
            "linz:film": item_dict["film"],
            "linz:film_sequence_no": item_dict["film_sequence_no"],
            "linz:photo_type": item_dict["photo_type"],
            "linz:format": item_dict["format"],
            "linz:source": item_dict["source"],
            "linz:physical_film_condition": item_dict["physical_film_condition"],
            "linz:image_anomalies": item_dict["image_anomalies"],
            "linz:scanned": item_dict["scanned"],
            "linz:raw_filename": item_dict["raw_filename"],
            "linz:released_filename": item_dict["released_filename"],
            "linz:when_scanned": item_dict["when_scanned"],
            "linz:photo_version": item_dict["photo_version"],
        }
        item.stac_item.properties.update(properties)
        item.stac_item.id = item_dict["sufi"]
        item.asset_basename = f"{item_dict['survey']}/{item_dict['sufi']}"
        item.metadata_file = f"{item_dict['survey']}/{item_dict['sufi']}.json"

    def read_csv(self):
        self.csv_dict = {}
        csv_path = os.path.join(os.getcwd(), "test_data", "historical_aerial_photos_metadata.csv")
        if not os.path.isfile(csv_path):
            raise Exception('Missing "historical_aerial_photos_metadata.csv"')

        with open(csv_path, "r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                released_filename = row["released_filename"]
                if released_filename in self.csv_dict:
                    raise Exception(f'Duplicate file "{released_filename}" found in metadata csv')
                self.csv_dict[released_filename] = row

        self.is_init = True
