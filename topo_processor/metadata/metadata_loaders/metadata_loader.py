from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from topo_processor.stac import Asset


class MetadataLoader(ABC):
    @property
    @abstractmethod
    def name(self):
        str

    @abstractmethod
    def is_applicable(self, asset: Asset) -> bool:
        pass

    @abstractmethod
    async def load_metadata(self, asset: Asset):
        pass
