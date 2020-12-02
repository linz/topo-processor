from typing import List

from linz_logger import get_log

from topo_processor.metadata.item import Item
from topo_processor.util.time import time_in_ms

from .metadata_loader import MetadataLoader


class MetadataLoaderRepository:
    loaders: List[MetadataLoader] = []

    def append(self, loader: MetadataLoader) -> None:
        self.loaders.append(loader)

    def add_metadata(self, item: Item) -> None:
        for loader in self.loaders:
            if loader.is_applicable(item):
                start_time = time_in_ms()
                loader.add_metadata(item)
                get_log().debug("Metadata added", loader=loader.name, duration=time_in_ms() - start_time, path=item.path)
