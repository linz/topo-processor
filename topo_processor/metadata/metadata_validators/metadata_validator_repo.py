from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List

from linz_logger import get_log

from topo_processor.util import time_in_ms

from .metadata_validator import MetadataValidator

if TYPE_CHECKING:
    from topo_processor.stac import Item


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
                    except Exception as e:
                        item.add_error(str(e), validator.name, e)
                        get_log().warning(f"Validation Failed: {e}", validator=validator.name)
                    get_log().debug(
                        "Validity Checked",
                        validator=validator.name,
                        duration=time_in_ms() - start_time,
                    )
