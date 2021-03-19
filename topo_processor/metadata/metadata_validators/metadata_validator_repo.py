import asyncio
import os
from typing import List

from linz_logger import get_log

from topo_processor.stac.item import Item
from topo_processor.util.time import time_in_ms

from .metadata_validator import MetadataValidator


class MetadataValidatorRepository:
    validators: List[MetadataValidator] = []
    lock = asyncio.Semaphore(5)

    def append(self, validator: MetadataValidator) -> None:
        self.validators.append(validator)

    async def validate_metadata(self, item: Item) -> None:
        async with self.lock:
            for validator in self.validators:
                if validator.is_applicable(item):
                    start_time = time_in_ms()
                    try:
                        await validator.validate_metadata(item)
                    except Exception as error_msg:
                        item.is_valid = False
                        get_log().warning(
                            f"Item not valid: {error_msg}", validator=validator.name, source_path=item.source_path
                        )
                    get_log().debug(
                        "Validity Checked",
                        validator=validator.name,
                        duration=time_in_ms() - start_time,
                        output_filename=os.path.join(item.parent, f"{item.id}{item.file_ext}"),
                    )
