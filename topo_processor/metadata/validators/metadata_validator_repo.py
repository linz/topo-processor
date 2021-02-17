import asyncio
from typing import List

from linz_logger import get_log

from topo_processor.factory.item import Item
from topo_processor.util.time import time_in_ms

from .metadata_validator import MetadataValidator


class MetadataValidatorRepository:
    validators: List[MetadataValidator] = []
    lock = asyncio.Semaphore(5)

    def append(self, loader: MetadataValidator) -> None:
        self.validators.append(loader)

    async def check_validity(self, item: Item) -> None:
        async with self.lock:
            for validator in self.validators:
                if validator.is_applicable(item):
                    start_time = time_in_ms()
                    await validator.check_validity(item)
                    get_log().debug(
                        "Validity Checked",
                        validator=validator.name,
                        duration=time_in_ms() - start_time,
                        collection=item.collection.stac_collection.id,
                        output_filename=item.item_output_path,
                    )
