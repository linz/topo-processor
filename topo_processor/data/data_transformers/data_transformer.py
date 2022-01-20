from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from topo_processor.stac.item import Item


class DataTransformer(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    def transform_data(self, item: Item) -> None:
        pass
