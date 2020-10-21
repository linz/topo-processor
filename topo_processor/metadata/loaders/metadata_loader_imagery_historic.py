import csv
import os

from topo_processor.metadata.data_type import DataType
from topo_processor.metadata.item import Item
from topo_processor.util import is_tiff

from .metadata_loader import MetadataLoader


class MetadataLoaderImageryHistoric(MetadataLoader):
    name = "loader.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.collection.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.path):
            return False
        return True

    def add_metadata(self, item: Item) -> None:
        file_name = os.path.splitext(os.path.basename(item.path))[0]
        csv_path = os.path.join(os.getcwd(), "historical_aerial_photos_metadata.csv")

        if not os.path.isfile(csv_path):
            raise Exception('Missing "historical_aerial_photos_metadata.csv"')

        with open(csv_path, "r") as fd:
            csv_file = csv.reader(fd, delimiter=",")
            metadata_keys = next(csv_file)
            file_name_index = metadata_keys.index("released_filename")

            has_found_file = False
            for row in csv_file:
                if file_name != row[file_name_index]:
                    continue
                if has_found_file:
                    raise Exception(f'Duplicate file "{file_name}" found in metadata csv')
                has_found_file = True
                properties = {
                    "linz:sufi": metadata_keys.index("sufi"),
                    "linz:survey": metadata_keys.index("survey"),
                    "linz:run": metadata_keys.index("run"),
                    "linz:photo_no": metadata_keys.index("photo_no"),
                    "linz:alternate_survey_name": metadata_keys.index("alternate_survey_name"),
                    "linz:camera": metadata_keys.index("camera"),
                    "linz:nominal_focal_length": metadata_keys.index("nominal_focal_length"),
                    "linz:altitude": metadata_keys.index("altitude"),
                    "linz:scale": metadata_keys.index("scale"),
                    "linz:date": metadata_keys.index("date"),
                    "linz:format": metadata_keys.index("format"),
                    "linz:released_filename": metadata_keys.index("released_filename"),
                    "linz:photo_version": metadata_keys.index("photo_version"),
                }
                item.stac_item.properties.update(properties)
