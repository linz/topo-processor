from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from topo_processor.stac import Asset


class MetadataLoader(ABC):
    @property
    @abstractmethod
    def name(self) -> Optional[str]:
        pass

    @abstractmethod
    def is_applicable(self, asset: Asset) -> bool:
        pass

    @abstractmethod
    def load_metadata(self, asset: Asset = None) -> None:
        pass
