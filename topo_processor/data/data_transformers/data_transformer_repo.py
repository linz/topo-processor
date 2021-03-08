import asyncio
from typing import List

from linz_logger import get_log

from topo_processor.stac.item import Item
from topo_processor.util.time import time_in_ms

from .data_transformer import DataTransformer


class DataTransformerRepository:
    transformers: List[DataTransformer] = []
    lock = asyncio.Semaphore(5)

    def append(self, transformers: DataTransformer) -> None:
        self.transformers.append(transformers)

    async def transform_data(self, item: Item) -> None:
        async with self.lock:
            for transformers in self.transformers:
                if transformers.is_applicable(item):
                    start_time = time_in_ms()
                    await transformers.transform_data(item)
                    get_log().debug(
                        "Data Compressed",
                        duration=time_in_ms() - start_time,
                    )
