import asyncio
from typing import List

from linz_logger import get_log

from topo_processor.stac.item import Item
from topo_processor.util.time import time_in_ms

from .metadata_validator import MetadataValidator


class MetadataValidatorRepository:
    validators: List[MetadataValidator] = []
    lock = asyncio.Semaphore(5)

    def append(self, loader: MetadataValidator) -> None:
        self.validators.append(loader)

    async def validate_metadata(self, item: Item) -> None:
        async with self.lock:
            for validator in self.validators:
                if validator.is_applicable(item):
                    start_time = time_in_ms()
                    await validator.validate_metadata(item)
                    get_log().debug(
                        "Validity Checked",
                        validator=validator.name,
                        duration=time_in_ms() - start_time,
                        output_filename=item.metadata_path,
                    )
