import os

from linz_logger import get_log

from topo_processor.stac.collection_store import CollectionStore
from topo_processor.stac.data_type import DataType
from topo_processor.stac.item import Item
from topo_processor.util.tiff import is_tiff

from .metadata_validator import MetadataValidator


class MetadataValidatorImageryHistoric(MetadataValidator):
    name = "validator.imagery.historic"

    def is_applicable(self, item: Item) -> bool:
        if item.data_type != DataType.ImageryHistoric:
            return False
        if not is_tiff(item.source_path):
            return False
        return True

    async def validate_metadata(self, item: Item) -> None:
        title = item.properties["linz:survey"]
        parent_folder = os.path.basename(os.path.dirname(item.source_path))
        if not parent_folder == title:
            get_log().info(
                "Metadata survey does not match image parent folder",
                metadata_survey=title,
                parent_folder=parent_folder,
                source_file=item.source_path,
            )
        store = CollectionStore()
        collection = store.get_collection(title)
        item.collection = collection
        item.collection.metadata_path = f"{item.properties['linz:survey']}/collection.json"
        collection.items.append(item)
