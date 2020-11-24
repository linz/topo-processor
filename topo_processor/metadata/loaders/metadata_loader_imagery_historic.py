import csv
import os
from typing import Dict

from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.item import Item
from topo_processor.util import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderImageryHistoric(MetadataLoader):
    name = "loader.imagery.historic"
    is_init = False
    csv_dict: Dict[str, Dict[str, str]] = {}

    def is_applicable(self, item: Item) -> bool:
        if item.collection.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.path):
            return False
        return True

    def add_metadata(self, item: Item) -> None:
        if not self.is_init:
            self.read_csv()

        item_path_basename = os.path.splitext(os.path.basename(item.path))[0]
        if item_path_basename not in self.csv_dict:
            raise Exception(f"{item_path_basename} cannot be found in the csv.")
        item_dict = self.csv_dict[item_path_basename]
        properties = {
            "linz:sufi": item_dict["sufi"],
            "linz:survey": item_dict["survey"],
            "linz:run": item_dict["run"],
            "linz:photo_no": item_dict["photo_no"],
            "linz:alternate_survey_name": item_dict["alternate_survey_name"],
            "linz:camera": item_dict["camera"],
            "linz:nominal_focal_length": item_dict["nominal_focal_length"],
            "linz:altitude": item_dict["altitude"],
            "linz:scale": item_dict["scale"],
            "linz:date": item_dict["date"],
            "linz:format": item_dict["format"],
            "linz:released_filename": item_dict["released_filename"],
            "linz:photo_version": item_dict["photo_version"],
        }
        item.stac_item.properties.update(properties)

    def read_csv(self):
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
