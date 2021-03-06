import asyncio
from typing import List

from linz_logger import get_log

from topo_processor.stac.item import Item
from topo_processor.util.time import time_in_ms

from .metadata_loader import MetadataLoader


class MetadataLoaderRepository:
    loaders: List[MetadataLoader] = []
    lock = asyncio.Semaphore(5)

    def append(self, loader: MetadataLoader) -> None:
        self.loaders.append(loader)

    async def add_metadata(self, item: Item) -> None:
        async with self.lock:
            for loader in self.loaders:
                if loader.is_applicable(item):
                    start_time = time_in_ms()
                    try:
                        await loader.add_metadata(item)
                    except Exception as error_msg:
                        item.is_valid = False
                        get_log().debug(f"Item not valid: {error_msg}", loader=loader.name, source_path=item.source_path)
                        return
                    get_log().debug(
                        "Metadata Added",
                        loader=loader.name,
                        duration=time_in_ms() - start_time,
                        metadata_path=item.metadata_path,
                    )
