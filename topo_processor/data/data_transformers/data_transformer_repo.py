from __future__ import annotations

from typing import TYPE_CHECKING, List

from linz_logger import get_log

from topo_processor.util.time import time_in_ms

from .data_transformer import DataTransformer

if TYPE_CHECKING:
    from topo_processor.stac.item import Item


class DataTransformerRepository:
    transformers: List[DataTransformer] = []

    def append(self, transformers: DataTransformer) -> None:
        self.transformers.append(transformers)

    def transform_data(self, item: Item) -> None:
        for transformer in self.transformers:
            if transformer.is_applicable(item):
                start_time = time_in_ms()
                try:
                    transformer.transform_data(item)
                except Exception as e:
                    item.add_error(str(e), transformer.name, e)
                    get_log().error("Data Transform Failed. Process is stopped.", transformers=transformer.name, error=e)
                    raise Exception(e)
                get_log().debug(
                    "Data Transformed",
                    duration=time_in_ms() - start_time,
                )
