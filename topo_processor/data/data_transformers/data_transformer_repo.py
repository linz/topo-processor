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
                    try:
                        await transformers.transform_data(item)
                    except Exception as error_msg:
                        item.is_valid = False
                        item.error_msgs.append(str(error_msg))
                        get_log().warning(
                            f"Transform Failed: {error_msg}", transformers=transformers.name, source_path=item.source_path
                        )
                        return False
                    get_log().debug(
                        "Data Transformed",
                        duration=time_in_ms() - start_time,
                    )
