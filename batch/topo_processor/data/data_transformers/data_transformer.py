from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from topo_processor.stac import Item


class DataTransformer(ABC):
    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        pass

    @abstractmethod
    def is_applicable(self, item: Item) -> bool:
        pass

    @abstractmethod
    def transform_data(self, item: Item) -> None:
        pass
