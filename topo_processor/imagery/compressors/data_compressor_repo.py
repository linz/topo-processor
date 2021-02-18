import asyncio
from typing import List

from linz_logger import get_log

from topo_processor.factory.item import Item
from topo_processor.util.time import time_in_ms

from .data_compressor import DataCompressor


class DataCompressorRepository:
    compressors: List[DataCompressor] = []
    lock = asyncio.Semaphore(5)

    def append(self, compressor: DataCompressor) -> None:
        self.compressors.append(compressor)

    async def compress_data(self, item: Item) -> None:
        async with self.lock:
            for compressor in self.compressors:
                if compressor.is_applicable(item):
                    start_time = time_in_ms()
                    await compressor.compress_data(item)
                    get_log().debug(
                        "Data Compressed",
                        duration=time_in_ms() - start_time,
                    )
